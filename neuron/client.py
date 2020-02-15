from .thought import Thought
import click
import socket
import struct
import time


# @click.command
# @click.option('-h', '--host', default='127.0.0.1', help='neuron server URL')
# @click.option('-p', '--port', default=8000, help='neuron server URL')
# @click.argument('path')
# def upload_sample(host, port, path):
#     address = host, port
#     sample = parse_sample(path)
#     upload_thought(address, int(user), thought)
@click.command
@click.argument('address')
@click.argument('user')
@click.argument('thought')
def upload(address, user, thought):
    ip, port = address.split(':')
    address = ip, int(port)
    upload_thought(address, int(user), thought)


def upload_thought(address, user_id, thought):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    thought = Thought(user_id, time.time(), thought)
    msg = thought.serialize()
    sock.sendall(msg)
    print('done')


def serialize_message(user_id, thought):
    msg = bytes()
    msg += struct.pack('<Q', user_id)
    msg += struct.pack('<Q', round(time.time()))
    thought = thought.encode('utf-8')
    msg += struct.pack('<I', len(thought))
    msg += thought
    return msg

