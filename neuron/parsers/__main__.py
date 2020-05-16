from .parsers import parse
import click
import json


_SNAPSHOTS_EXCHANGE = 'snapshots'
_RESULTS_EXCHANGE = 'results'


@click.group()
def cli():
    pass


@cli.command(name='parse')
@click.argument('parser', type=str)
@click.argument('data', type=click.File('rb'))
def command_parse(parser, data):
    try:
        snapshot = json.load(data)
    except:
        print('An error occurred. Bad JSON input.')
        exit(1)

    try:
        res = parse(parser, snapshot)
    except:
        print('An error occurred. Failed to parse input snapshot.')
        exit(1)

    print(json.dumps(res))


@cli.command(name='run-parser')
@click.argument('parser', type=str)
@click.argument('msgqueue_url')
def command_run_parser(parser, msgqueue_url):
    import pika
    import uuid
    if msgqueue_url.startswith('rabbitmq://'):
        url = msgqueue_url[len('rabbitmq://'):]
        host, port = url.split(':')
        port = int(port)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        channel = connection.channel()
        res = channel.queue_declare(queue=f'parser_{parser}_{uuid.uuid1()}', auto_delete=True)
        queue = res.method.queue
        channel.queue_bind(exchange=_SNAPSHOTS_EXCHANGE, queue=queue, routing_key='#')
        channel.exchange_declare(exchange=_RESULTS_EXCHANGE, exchange_type='topic')

        for _, _, body in channel.consume(queue, auto_ack=True):
            try:
                snapshot = json.loads(body)
                res = parse(parser, snapshot)

                msg = json.dumps(res)
                channel.basic_publish(exchange=_RESULTS_EXCHANGE, routing_key=parser, body=msg)
            except Exception:
                print('Failed to parse data')
                break

        channel.close()
        connection.close()
    else:
        print('Unsupported message queue type.')
        exit(1)


if __name__ == '__main__':
    cli(prog_name='neuron.parsers')
