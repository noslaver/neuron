import json
import pika


class RabbitHandler:
    def __init__(self, url):
        self.url = url
        host, port = url.split(':')
        port = int(port)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=_SNAPSHOTS_EXCHANGE, exchange_type='topic')

    def handle(self, snapshot):
        msg = json.dumps(snapshot)
        self.channel.basic_publish(exchange=_SNAPSHOTS_EXCHANGE, routing_key='', body=msg)
