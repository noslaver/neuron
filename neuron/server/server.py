from ..protobuf import neuron_pb2
from ..protocol import Snapshot, Image, Feelings, Pose
import datetime as dt
from flask import Flask, request
from pathlib import Path


app = Flask(__name__)

_RAW_DIR = 'raw'


@app.route('/users/<user_id>/snapshots', methods=['POST'])
def snapshot(user_id):
    snap = neuron_pb2.Snapshot()
    snap.ParseFromString(request.data)

    color_image = snap.color_image
    depth_image = snap.depth_image

    date = dt.datetime.fromtimestamp(snap.datetime / 1000.0)

    directory = Path(_RAW_DIR) / str(user_id) / date.strftime('%Y-%m-%d_%H-%M-%S-%f')
    directory.mkdir(parents=True, exist_ok=True)

    color_image_path = str(directory / 'color_image')
    depth_image_path = str(directory / 'depth_image')

    with open(color_image_path, 'wb') as writer:
        writer.write(color_image.data)

    with open(depth_image_path, 'wb') as writer:
        writer.write(color_image.data)

    translation = snap.pose.translation
    translation = {'x': translation.x, 'y': translation.y, 'z': translation.z}

    rotation = snap.pose.rotation
    rotation = {'x': rotation.x, 'y': rotation.y, 'z': rotation.z, 'w': rotation.w}

    feelings = snap.feelings

    snapshot = {
                'user_id': user_id, #TODO - entire user
                'timestamp': snap.datetime,
                'pose': {
                    'translation': translation,
                    'rotation': rotation,
                },
                'color_image': {
                    'height': color_image.height,
                    'width': color_image.width,
                    'path': color_image_path,
                    },
                'depth_image': {
                    'height': depth_image.height,
                    'width': depth_image.width,
                    'path': depth_image_path,
                },
                'feelings': {
                    'hunger': feelings.hunger,
                    'thirst': feelings.thirst,
                    'exhaustion': feelings.exhaustion,
                    'happiness': feelings.happiness
                }
            }

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
