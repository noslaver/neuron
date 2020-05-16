import click
import json
import requests


def print_result(data):
    data = json.loads(data)
    print(json.dumps(data, indent=4, sort_keys=True))


def get(host, port, url):
    if not url.startswith('/'):
        url += '/'
    url = f'http://{host}:{port}{url}'
    response = requests.get(url)

    data = json.loads(response.content)

    print_result(response.content)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_users(host, port):
    get(host, port, '/users')


@cli.command()
@click.argument('user_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_user(user_id, host, port):
    get(host, port, f'/users/{user_id}')


@cli.command()
@click.argument('user_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_snapshots(user_id, host, port):
    get(host, port, f'/users/{user_id}/snapshots')


@cli.command()
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def get_snapshot(user_id, snapshot_id, host, port):
    get(host, port, f'/users/{user_id}/snapshots/{snapshot_id}')


@cli.command()
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('result_id')
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
@click.option('--save', '-s', 'path', help='save result to path',
              type=click.File('wb'))
def get_result(user_id, snapshot_id, result_id, path, host, port):
    get(host, port, f'/users/{user_id}/snapshots/{snapshot_id}/{result_id}')


if __name__ == '__main__':
    cli(prog_name='neuron.cli')
