from ..protobuf import neuron_pb2
from .reader import Reader
import requests


def upload_sample(host, port, path):
    reader = Reader(path, 'protobuf')

    server_url = f'http://{host}:{port}'

    for index, snapshot in enumerate(reader.read()):
        # TODO - use logger
        print(f'Uploading snapshot #{index + 1}')

        request = neuron_pb2.SnapshotInfo()
        request.snapshot.CopyFrom(snapshot)
        request.user.CopyFrom(reader.user)

        data = request.SerializeToString()
        headers = {'Content-Type': 'application/protobuf'}

        response = requests.post(
            f'{server_url}/users/{request.user.user_id}/snapshots', data=data, headers=headers)

        if response.status_code != 204:
            print('Error uploading snapshot to server')
            exit(1)
