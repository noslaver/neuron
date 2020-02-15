from .thought import Thought
from .utils import Connection
import datetime as dt


# @click.command
# @click.option('-h', '--host', default='127.0.0.1', help='neuron server URL')
# @click.option('-p', '--port', default=8000, help='neuron server URL')
# @click.argument('path')
# def upload_sample(host, port, path):
#     address = host, port
#     sample = parse_sample(path)
#     upload_thought(address, int(user), thought)
def upload_thought(address, user_id, thought):
    conn = Connection.connect(*address)
    with conn:
        thought = Thought(user_id, dt.datetime.now(), thought)
        msg = thought.serialize()
        conn.send(msg)
