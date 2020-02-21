from .client import upload_thought
from .server import run_server
from .reader import Reader
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


@cli.command()
@click.argument('path')
def read(path):
    reader = Reader(path)
    print(f'user {reader.user_id}: {reader.username}, born {reader.birthdate} ({reader.gender})')
    for snapshot in reader:
        print(snapshot)


if __name__ == '__main__':
    cli(prog_name='neuron')
