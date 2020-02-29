from .parsers import run_parser
import click
import pika
import uuid


_SNAPSHOTS_EXCHANGE = 'snapshots'


@click.group()
def cli():
    pass


@cli.command(name='parse')
@click.argument('parser', type=str)
@click.argument('data', type=click.File('rb'))
def command_parse(parser, data):
    res = run_parser(parser, data)
    print(res)


@cli.command(name='run-parser')
@click.argument('parser', type=str)
@click.argument('msgqueue_url')
def command_run_parser(parser, msgqueue_url):
    if msgqueue_url.startswith('rabbitmq://'):
        url = msgqueue_url[len('rabbitmq://'):]
        host, port = url.split(':')
        port = int(port)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        channel = connection.channel()
        res = channel.queue_declare(queue=f'parser_{parser}_{uuid.uuid1()}', auto_delete=True)
        queue = res.method.queue
        channel.queue_bind(exchange=_SNAPSHOTS_EXCHANGE, queue=queue, routing_key='#')

        for _, _, body in channel.consume(queue):
            try:
                run_parser(parser, body)
            except Exception:
                print('Failed to parse data')
                break

        channel.close()
        connection.close()


if __name__ == '__main__':
    cli(prog_name='neuron.parsers')
