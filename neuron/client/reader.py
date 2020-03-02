import datetime as dt
import struct

from ..protobuf import neuron_pb2
from ..protocol import Image, Feelings, Snapshot


def read_int(fp):
    return int.from_bytes(fp.read(4), 'little')


def read_long(fp):
    return int.from_bytes(fp.read(8), 'little')


def read_double(fp):
    return struct.unpack('d', fp.read(8))[0]


def read_float(fp):
    return struct.unpack('f', fp.read(4))[0]


class BinaryParser:
    def parse_user_info(self, fp):
        user_id = read_long(fp)

        name_len = read_int(fp)
        username = fp.read(name_len).decode('utf-8')

        birthdate = dt.datetime.fromtimestamp(read_int(fp))

        gender = fp.read(1).decode('utf-8')

        return (user_id, username, birthdate, gender)

    def parse_snapshot(self, fp):
        timestamp = dt.datetime.fromtimestamp(read_long(fp) / 1000.0)

        x = read_double(fp)
        y = read_double(fp)
        z = read_double(fp)
        translation = (x, y, z)

        x = read_double(fp)
        y = read_double(fp)
        z = read_double(fp)
        w = read_double(fp)
        rotation = (x, y, z, w)

        height = read_int(fp)
        width = read_int(fp)
        # TODO - convert BGR to RGB
        image_pixels = fp.read(height * width * 3)
        color_image = Image('color', height, width, image_pixels)

        height = read_int(fp)
        width = read_int(fp)
        image_depths = fp.read(height * width * 4)
        depth_image = Image('depth', height, width, image_depths)

        hunger = read_float(fp)
        thirst = read_float(fp)
        exhaustion = read_float(fp)
        happiness = read_float(fp)
        feelings = Feelings(hunger, thirst, exhaustion, happiness)

        return Snapshot(timestamp, translation, rotation, color_image,
                        depth_image, feelings)


class ProtobufParser:
    def parse_user_info(self, fp):
        length = read_int(fp)
        data = fp.read(length)
        user = neuron_pb2.User()
        user.ParseFromString(data)

        return user

    def parse_snapshot(self, fp):
        length = read_int(fp)
        if length == 0:
            return None
        data = fp.read(length)

        snap = neuron_pb2.Snapshot()
        snap.ParseFromString(data)
        return snap


class Reader:
    def __init__(self, path, protocol):
        self.path = path
        if protocol == 'binary':
            self.fp = open(path, 'rb')
            self.parser = BinaryParser()
        if protocol == 'protobuf':
            import gzip
            self.fp = gzip.open(path, 'rb')
            self.parser = ProtobufParser()

    def read(self):
        self.user = self.parser.parse_user_info(self.fp)
        while True:
            try:
                snapshot = self.parser.parse_snapshot(self.fp)
                if snapshot is None:
                    break
                yield snapshot
            except ValueError:
                self.fp.close()
                break
