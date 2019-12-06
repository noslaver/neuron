from cli import CommandLineInterface
import socket
import struct
import time
from thought import Thought


cli = CommandLineInterface()

@cli.command
def upload(address, user, thought):
    ip, port = address.split(':')
    address = ip, int(port)
    upload_thought(address, int(user), thought)


def upload_thought(address, user_id, thought):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    thought = Thought(user_id, time.time(), thought)
    msg = thought.serializ()
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


def main(argv):
    cli.main()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
