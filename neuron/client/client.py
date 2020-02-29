from .reader import Reader
import requests


def upload_sample(host, port, path):
    reader = Reader(path, 'protobuf')

    server_url = f'http://{host}:{port}'

    for index, snapshot in enumerate(reader.read()):
        # TODO - use logger
        print(f'Uploading snapshot #{index + 1}')
        sp = snapshot.SerializeToString()
        headers = {'Content-Type': 'application/protobuf'}
        response = requests.post(f'{server_url}/users/{reader.user_id}/snapshots', data=sp, headers=headers)
