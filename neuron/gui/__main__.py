from .gui import run_server as run
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', help='server\'s IP', default='127.0.0.1')
@click.option('--port', '-p', help='server\'s port', type=int, default=8000)
@click.option('--api-host', '-H', help='API server\'s IP', default='127.0.0.1')
@click.option('--api-port', '-P', help='API server\'s port', type=int, default=5000)
def run_server(host, port, api_host, api_port):
    run(host, port, api_host, api_port)


if __name__ == '__main__':
    cli(prog_name='neuron.api')
