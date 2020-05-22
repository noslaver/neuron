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

    if response.status_code != 200:
        return None

    data = json.loads(response.content)
    return data


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=5000)
def get_users(host, port):
    data = get(host, port, '/users')
    print_result(data)


@cli.command()
@click.argument('user_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=5000)
def get_user(user_id, host, port):
    data = get(host, port, f'/users/{user_id}')
    print_result(data)


@cli.command()
@click.argument('user_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=5000)
def get_snapshots(user_id, host, port):
    data = get(host, port, f'/users/{user_id}/snapshots')
    print_result(data)


@cli.command()
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=5000)
def get_snapshot(user_id, snapshot_id, host, port):
    data = get(host, port, f'/users/{user_id}/snapshots/{snapshot_id}')
    print_result(data)


@cli.command()
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('result_id')
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=5000)
@click.option('--save', '-s', 'path', help='save result to path',
              type=click.File('wb'))
def get_result(user_id, snapshot_id, result_id, path, host, port):
    data = get(host, port, f'/users/{user_id}/snapshots/{snapshot_id}/{result_id}')
    print_result(data)


if __name__ == '__main__':
    cli(prog_name='neuron.cli')
