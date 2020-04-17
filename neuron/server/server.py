from ..protobuf import neuron_pb2
import datetime as dt
from flask import Flask, request
from pathlib import Path
import struct


app = Flask(__name__)

_RAW_DIR = Path('raw')


def message_handler(message):
    pass


@app.route('/users/<user_id>/snapshots', methods=['POST'])
def snapshot(user_id):
    if request.data == b'':
        return ('', 400)

    try:
        data = neuron_pb2.SnapshotInfo()
        data.ParseFromString(request.data)
    except ValueError:
        return ('', 400)

    snap = data.snapshot
    user = data.user

    color_image = snap.color_image
    depth_image = snap.depth_image

    date = dt.datetime.fromtimestamp(snap.datetime / 1000.0)

    directory = _RAW_DIR / str(user_id) / date.strftime('%Y-%m-%d_%H-%M-%S-%f')
    directory.mkdir(parents=True, exist_ok=True)

    color_image_path = str(directory / 'color_image')
    depth_image_path = str(directory / 'depth_image')

    with open(color_image_path, 'wb') as writer:
        writer.write(color_image.data)

    with open(depth_image_path, 'wb') as writer:
        data = list(depth_image.data)
        writer.write(struct.pack(f'{len(data)}f', *data))

    translation = snap.pose.translation
    translation = {'x': translation.x, 'y': translation.y, 'z': translation.z}

    rotation = snap.pose.rotation
    rotation = {'x': rotation.x, 'y': rotation.y, 'z': rotation.z, 'w': rotation.w}

    feelings = snap.feelings

    if user.gender == 0:
        gender = 'Male'
    if user.gender == 1:
        gender = 'Female'
    if user.gender == 2:
        gender = 'Other'

    snapshot = {
                'user': {
                    'id': user_id,
                    'name': user.username,
                    'birthday': user.birthday,
                    'gender': gender
                },
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




def run_server(host, port, publish):
    global message_handler
    global _RAW_DIR
    message_handler = publish
    app.run(host=host, port=port)
