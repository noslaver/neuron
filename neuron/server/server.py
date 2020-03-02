from ..protobuf import neuron_pb2
from ..protocol import Snapshot, Image, Feelings, Pose
import datetime as dt
from flask import Flask, request
from pathlib import Path


app = Flask(__name__)

_DATA_DIR = 'data'


@app.route('/users/<user_id>/snapshots', methods=['POST'])
def snapshot(user_id):
    snap = neuron_pb2.Snapshot()
    snap.ParseFromString(request.data)

    # TODO - save binary data to disk
    color_image = snap.color_image
    depth_image = snap.depth_image

    directory = Path(_DATA_DIR) / str(user_id) / \
        snap.datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
    directory.mkdir(parents=True, exist_ok=True)

    color_image_path = directory / 'color_image'
    depth_image_path = directory / 'depth_image'

    with open(color_image_path, 'w') as writer:
        writer.write(color_image.content)

    with open(depth_image_path, 'w') as writer:
        writer.write(color_image.content)

    timestamp = dt.datetime.fromtimestamp(snap.datetime / 1000.0)

    translation = snap.pose.translation
    translation = (translation.x, translation.y, translation.z)

    rotation = snap.pose.rotation
    rotation = (rotation.x, rotation.y, rotation.z, rotation.w)

    pose = Pose(translation, rotation)

    color_image = Image('color', color_image.height, color_image.width,
                        color_image_path)
    depth_image = Image('depth', depth_image.height, depth_image.width,
                        depth_image_path)

    feelings = snap.feelings
    feelings = Feelings(feelings.hunger, feelings.thirst, feelings.exhaustion,
                        feelings.happiness)

    snapshot = Snapshot(timestamp, pose, color_image, depth_image, feelings)

    message_handler(snapshot)

    return ('', 204)


def message_handler():
    pass


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
