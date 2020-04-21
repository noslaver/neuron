import json
import pika


_SNAPSHOTS_EXCHANGE = 'snapshots'


class RabbitHandler:
    def __init__(self, url):
        host, port = url.split(':')
        self.host = host
        self.port = int(port)

    def handle(self, snapshot):
        msg = json.dumps(snapshot)
        self.channel.basic_publish(exchange=_SNAPSHOTS_EXCHANGE, routing_key='', body=msg)

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=_SNAPSHOTS_EXCHANGE, exchange_type='topic')

    def close(self):
        self.connection.close()
