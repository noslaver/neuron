from .server import Saver
import click
import pika


_RESULTS_EXCHANGE = 'results'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('parser')
@click.argument('data', type=click.File('rb'))
@click.option('-d', '--database', 'db_url', help='database URL', default='postgresql://127.0.0.1:5432')
def run_saver(parser, data, db_url):
    saver = Saver(db_url)
    saver.save(parser, data)


@cli.command()
@click.argument('db_url')
@click.argument('msgqueue_url')
def run_saver(db_url, msgqueue_url):
    saver = Saver(db_url)

    if msgqueue_url.startswith('rabbitmq://'):
        url = msgqueue_url[len('rabbitmq://'):]
        host, port = url.split(':')
        port = int(port)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        channel = connection.channel()
        res = channel.queue_declare(queue=f'saver_{parser}_{uuid.uuid1()}', auto_delete=True)
        queue = res.method.queue
        channel.queue_bind(exchange=_RESULTS_EXCHANGE, queue=queue, routing_key=parser)

        for _, _, body in channel.consume(queue):
            try:
                saver.save(parser, body)
            except Exception:
                print('Failed to parse data')
                break

        channel.close()
        connection.close()


class RabbitHandler:
    def __init__(self, url):
        self.url = url
        host, port = url.split(':')
        port = int(port)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=_SNAPSHOTS_EXCHANGE, exchange_type='topic')

    def handle(self, snapshot):
        msg = snapshot.SerializeToString()
        self.channel.basic_publish(exchange=_SNAPSHOTS_EXCHANGE, routing_key='', body=msg)


def publish_to_rabbit(message):
    print(message)


if __name__ == '__main__':
    cli(prog_name='neuron.server')
