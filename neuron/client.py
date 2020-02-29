from .reader import Reader
from .utils import Connection
import requests


def upload_snapshot(address, path):
    reader = Reader(path, 'protobuf')


    for snapshot in reader.read():
        headers = {'Content-Type': 'application/protobuf'}
        response = requests.post(f'{server_url}/users/{reader.user_id}/snapshots', data=snapshot, headers=headers)
