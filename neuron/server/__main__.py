from .server import run_server as run
import click
import json
import pika


_SNAPSHOTS_EXCHANGE = 'snapshots'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('msgqueue_url')
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def run_server(msgqueue_url, host, port):
    if msgqueue_url.startswith('rabbitmq://'):
        handler = RabbitHandler(msgqueue_url[len('rabbitmq://'):])
    else:
        print('Unsupported message queue type.')
        exit(1)
    run(host, port, publish=handler.handle)


class RabbitHandler:
    def __init__(self, url):
        self.url = url
        host, port = url.split(':')
        port = int(port)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=_SNAPSHOTS_EXCHANGE, exchange_type='topic')

    def handle(self, snapshot):
        msg = json.dumps(snapshot)
        self.channel.basic_publish(exchange=_SNAPSHOTS_EXCHANGE, routing_key='', body=msg)


if __name__ == '__main__':
    cli(prog_name='neuron.server')
