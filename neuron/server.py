from .parsers import Parsers, ParseContext
from .protobuf import neuron_pb2
from .protocol import Config, Snapshot, Image, Feelings
from .utils.listener import Listener
import datetime as dt
from flask import Flask, request
from pathlib import Path


app = Flask(__name__)

data_dir = None

parsers = Parsers()
parsers.load_modules('neuron/parsers')

@app.route('/config', methods=['GET'])
def config():
    config = Config(list(parsers.parsers.keys()))

    return config.serialize()


@app.route('/users/<user_id>/snapshots', methods=['POST'])
def snapshot(user_id):
    snap = neuron_pb2.Snapshot()
    snap.ParseFromString(request.data)

    timestamp = dt.datetime.fromtimestamp(snap.datetime / 1000.0)

    translation = snap.pose.translation
    translation = (translation.x, translation.y, translation.z)

    rotation = snap.pose.rotation
    rotation = (rotation.x, rotation.y, rotation.z, rotation.w)

    color_image = snap.color_image
    color_image = Image('color', color_image.height, color_image.width, color_image.data)

    depth_image = snap.depth_image
    depth_image = Image('depth', depth_image.height, depth_image.width, depth_image.data)

    feelings = snap.feelings
    feelings = Feelings(feelings.hunger, feelings.thirst, feelings.exhaustion, feelings.happiness)

    snapshot = Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)

    directory = Path(data_dir) / str(user_id) / snapshot.timestamp.strftime('%Y-%m-%d_%H-%M-%S-%f')
    directory.mkdir(parents=True, exist_ok=True)

    for parser in parsers.parsers:
        parser(ParseContext(directory), snapshot)

    return ('', 204)


def run_server(address, directory):
    global data_dir
    data_dir = Path(directory)
    host, port = address
    app.run(host=host, port=port)


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    import signal
    import sys
    signal.signal(signal.SIGINT, signal_handler)
