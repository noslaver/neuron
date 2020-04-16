from .server import run_server as run
from .rabbit import RabbitHandler
import click


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


if __name__ == '__main__':
    cli(prog_name='neuron.server')
