from .api import run_api_server
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-H', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=5000)
@click.option('--database', '-d', 'db_url', help='database URL', default='mongodb://127.0.0.1:27017')
def run_server(host, port, db_url):
    run_api_server(host, port, db_url)


if __name__ == '__main__':
    cli(prog_name='neuron.api')
