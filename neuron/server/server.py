from ..protobuf import neuron_pb2
from ..protocol import Snapshot, Image, Feelings
import datetime as dt
from flask import Flask, request
from pathlib import Path


app = Flask(__name__)

message_handler = lambda *args: None

_DATA_DIR = 'data'


@app.route('/users/<user_id>/snapshots', methods=['POST'])
def snapshot(user_id):
    snapshot = neuron_pb2.Snapshot()
    snapshot.ParseFromString(request.data)

    # TODO - save binary data to disk
    #color_image = snapshot.color_image
    #depth_image= snapshot.depth_image

    #directory = Path(_DATA_DIR) / str(user_id) / snapshot.timestamp.strftime('%Y-%m-%d_%H-%M-%S-%f')
    #directory.mkdir(parents=True, exist_ok=True)

    message_handler(snapshot)

    return ('', 204)


def run_server(host, port, publish):
    global message_handler
    message_handler = publish
    app.run(host=host, port=port)


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    import signal
    import sys
    signal.signal(signal.SIGINT, signal_handler)
