import datetime as dt
import struct

from .protobuf import neuron_pb2
from .protocol import Image, Feelings, Snapshot


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

        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)


class ProtobufParser:
    def parse_user_info(self, fp):
        length = read_int(fp)
        data = fp.read(length)
        user = neuron_pb2.User()
        user.ParseFromString(data)

        birthdate = dt.datetime.fromtimestamp(user.birthday)
        if user.gender == 0:
            gender = 'm'
        if user.gender == 1:
            gender = 'f'
        if user.gender == 2:
            gender = 'o'

        return (user.user_id, user.username, birthdate, gender)

    def parse_snapshot(self, fp):
        length = read_int(fp)
        data = fp.read(length)
        snap = neuron_pb2.Snapshot()
        snap.ParseFromString(data)

        timestamp = dt.datetime.fromtimestamp(snap.datetime / 1000.0)

        translation = snap.pose.translation
        translation = (translation.x, translation.y, translation.z)

        rotation = snap.pose.rotation
        rotation = (rotation.x, rotation.y, rotation.z, rotation.w)

        color_image = snap.color_image
        color_image = Image('color', color_image.height, color_image.width, color_image.data)

        depth_image = snap.depth_image
        depth_image = Image('depth', depth_image.height, depth_image.width, depth_image.data)

        feelings = snap.feelings
        feelings = Feelings(feelings.hunger, feelings.thirst, feelings.exhaustion, feelings.happiness)

        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)


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

    def read_user_info(self):
        try:
            (self.user_id, self.username, self.birthdate, self.gender) = self.parser.parse_user_info(self.fp)
        except Exception:
            self.fp.close()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            snapshot = self.parser.parse_snapshot(self.fp)
            return snapshot
        except Exception:
            self.fp.close()
            raise StopIteration
    #
    # def read(self):
    #     while True:
    #         try:
    #             snapshot = self.parser.parse_snapshot(self.fp)
    #             yield snapshot
    #         except Exception:
    #             self.fp.close()
