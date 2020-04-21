from .rabbit import RabbitHandler
from .server import run_server as run
from ..utils import retry
import click
import time


@click.group()
def cli():
    pass


@cli.command()
@click.argument('msgqueue_url', required=False)
@click.option('--host', '-H', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
@click.option('--print', 'prnt', help='print published snapshots', is_flag=True, hidden=True)
def run_server(msgqueue_url, host, port, prnt):
    handler = None

    if msgqueue_url is not None and msgqueue_url.startswith('rabbitmq://'):
        handler = RabbitHandler(msgqueue_url[len('rabbitmq://'):])

        retry(handler.connect, times=5)

        publish = handler.handle
    elif prnt:
        publish = print
    else:
        print('Unsupported message queue type.')
        exit(1)

    try:
        run(host, port, publish=publish)
    except Exception as e:
        print(e)
        exit(1)
    finally:
        if handler is not None:
            handler.close()


if __name__ == '__main__':
    cli(prog_name='neuron.server')
