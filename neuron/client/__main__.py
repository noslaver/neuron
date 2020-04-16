import click
from .client import upload_sample as upload
import requests.exceptions


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--host', '-H', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
def upload_sample(path, host, port):
    try:
        upload(host, port, path)
    except requests.exceptions.ConnectionError:
        print('Failed to connect to server, exiting...')
        exit(1)
    except:
        print('An error occurred while uploading sample, aborting...')
        exit(2)


if __name__ == '__main__':
    cli(prog_name='neuron.client')
