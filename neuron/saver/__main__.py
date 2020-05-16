from .saver import Saver
import click
from collections import namedtuple
import json
import pika
import uuid


_RESULTS_EXCHANGE = 'results'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('parser')
@click.argument('data', type=click.File('rb'))
@click.option('-d', '--database', 'db_url', help='database URL', default='mongodb://127.0.0.1:27017')
def save(parser, data, db_url):
    saver = Saver(db_url)
    data = json.load(data)
    saver.save(parser, data)


@cli.command()
@click.argument('db_url')
@click.argument('msgqueue_url')
def run_saver(db_url, msgqueue_url):
    if not msgqueue_url.startswith('rabbitmq://'):
        print('Unsupported message queue type.')
        exit(1)

    saver = Saver(db_url)

    url = msgqueue_url[len('rabbitmq://'):]
    host, port = url.split(':')
    port = int(port)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()
    res = channel.queue_declare(queue=f'saver_{uuid.uuid1()}', auto_delete=True)
    queue = res.method.queue
    channel.queue_bind(exchange=_RESULTS_EXCHANGE, queue=queue, routing_key='#')

    for method, _, body in channel.consume(queue):
        try:
            parser = method.routing_key
            saver.save(parser, body)
        except Exception:
            print('Failed to save data')
            break

    channel.close()
    connection.close()


if __name__ == '__main__':
    cli(prog_name='neuron.saver')
