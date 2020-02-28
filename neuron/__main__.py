from .client import upload_snapshot
from .server import run_server
from .reader import Reader
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('address')
@click.argument('data')
def run(address, data):
    ip, port = address.split(':')
    address = ip, int(port)
    run_server(address, data)


@cli.command()
@click.argument('path')
@click.argument('address')
def read(path, address):
    ip, port = address.split(':')
    address = ip, int(port)
    upload_snapshot(address, path)


if __name__ == '__main__':
    cli(prog_name='neuron')
