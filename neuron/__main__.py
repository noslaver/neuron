from .client import upload_thought
from .server import run_server
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('address')
@click.argument('user')
@click.argument('thought')
def upload(address, user, thought):
    ip, port = address.split(':')
    address = ip, int(port)
    upload_thought(address, int(user), thought)
    print('done')


@cli.command()
@click.argument('address')
@click.argument('data')
def run(address, data):
    ip, port = address.split(':')
    address = ip, int(port)
    run_server(address, data)


if __name__ == '__main__':
    cli(prog_name='neuron')
