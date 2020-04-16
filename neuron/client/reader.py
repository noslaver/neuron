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

        birthday = read_int(fp)

        gender = fp.read(1).decode('utf-8')

        if gender == 'm':
            gender = 0
        elif gender == 'f':
            gender = 1
        else:
            gender = 2

        user = neuron_pb2.User()
        user.user_id = user_id
        user.username = username
        user.birthday = birthday
        user.gender = gender

        return user

    def parse_snapshot(self, fp):
        snapshot = neuron_pb2.Snapshot()

        datetime = read_long(fp)
        snapshot.datetime = datetime

        x = read_double(fp)
        y = read_double(fp)
        z = read_double(fp)

        pose = snapshot.pose
        trans = pose.translation
        trans.x, trans.y, trans.z = x, y, z

        x = read_double(fp)
        y = read_double(fp)
        z = read_double(fp)
        w = read_double(fp)

        rot = pose.rotation
        rot.x, rot.y, rot.z, rot.w = x, y, z, w

        height = read_int(fp)
        width = read_int(fp)
        image_pixels = fp.read(height * width * 3)

        color_image = snapshot.color_image
        color_image.height = height
        color_image.width = width
        color_image.data = image_pixels

        height = read_int(fp)
        width = read_int(fp)
        image_depths = fp.read(height * width * 4)

        depth_image = snapshot.depth_image
        depth_image.height = height
        depth_image.width = width
        depth_image.data.extend(image_depths)

        hunger = read_float(fp)
        thirst = read_float(fp)
        exhaustion = read_float(fp)
        happiness = read_float(fp)

        feelings = snapshot.feelings
        feelings.hunger = hunger
        feelings.thirst = thirst
        feelings.exhaustion = exhaustion
        feelings.happiness = happiness

        return snapshot


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

        self.user = None

    def read(self):
        self.user = self.parser.parse_user_info(self.fp)
        while True:
            try:
                snapshot = self.parser.parse_snapshot(self.fp)
                if snapshot is None:
                    break
                yield snapshot
            except (ValueError, struct.error):
                self.fp.close()
                break
