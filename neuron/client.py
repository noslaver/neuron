from .reader import Reader
from .utils import Connection
import requests


def upload_snapshot(address, path):
    reader = Reader(path, 'protobuf')

    server_url = f'http://{address[0]}:{address[1]}'

    for snapshot in reader.read():
        sp = snapshot.SerializeToString()
        headers = {'Content-Type': 'application/protobuf'}
        response = requests.post(f'{server_url}/users/{reader.user_id}/snapshots', data=sp, headers=headers)
