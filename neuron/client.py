from .protocol import Config, Hello
from .reader import Reader
from .utils import Connection
import datetime as dt


def upload_snapshot(address, path):
    reader = Reader(path)

    reader.read_user_info()

    hello = Hello(reader.user_id, reader.username, reader.birthdate, reader.gender)
    for snapshot in reader:
        with Connection.connect(*address) as conn:
            conn.send_message(hello.serialize())

            msg = conn.receive_message()
            config = Config.deserialize(msg)

            sp = snapshot.with_fields(config.fields)
            print(sp)
            conn.send_message(sp.serialize())
