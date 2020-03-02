import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_users(host, port):
    pass


@cli.command()
@click.argument('user_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_user(user_id, host, port):
    pass


@cli.command()
@click.argument('user_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_snapshots(user_id, host, port):
    pass


@cli.command()
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_snapshot(user_id, snapshot_id, host, port):
    pass


@cli.command()
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('result_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
@click.option('--save', '-s', 'path', help='save result to path',
              type=click.File('wb'))
def get_result(user_id, snapshot_id, result_id, path, host, port):
    pass


if __name__ == '__main__':
    cli(prog_name='neuron.cli')
