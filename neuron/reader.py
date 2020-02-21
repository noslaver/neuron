import datetime as dt
import struct

from .protocol import Image, Feelings, Snapshot


class Reader:
    def __init__(self, path):
        self.parse_user_info(path)

    def parse_user_info(self, path):
        self.sample = open(path, 'rb')
        try:
            self.user_id = self.read_long()
            name_len = self.read_int()
            self.username = self.sample.read(name_len).decode('utf-8')
            self.birthdate = dt.datetime.fromtimestamp(self.read_int())
            self.gender = self.sample.read(1).decode('utf-8')
        except Exception:
            self.sample.close()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            snapshot = self.parse_snapshot()
            return snapshot
        except Exception:
            self.sample.close()
            raise StopIteration

    def parse_snapshot(self):
        timestamp = dt.datetime.fromtimestamp(self.read_long() / 1000.0)

        x = self.read_double()
        y = self.read_double()
        z = self.read_double()
        translation = (x, y, z)

        x = self.read_double()
        y = self.read_double()
        z = self.read_double()
        w = self.read_double()
        rotation = (x, y, z, w)

        height = self.read_int()
        width = self.read_int()
        # TODO - convert BGR to RGB
        image_pixels = self.sample.read(height * width * 3)
        color_image = Image('color', height, width, image_pixels)

        height = self.read_int()
        width = self.read_int()
        image_depths = self.sample.read(height * width * 4)
        depth_image = Image('depth', height, width, image_depths)

        hunger = self.read_float()
        thirst = self.read_float()
        exhaustion = self.read_float()
        happiness = self.read_float()
        feelings = Feelings(hunger, thirst, exhaustion, happiness)

        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)

    def read_int(self):
        return int.from_bytes(self.sample.read(4), 'little')

    def read_long(self):
        return int.from_bytes(self.sample.read(8), 'little')

    def read_double(self):
        return struct.unpack('d', self.sample.read(8))

    def read_float(self):
        return struct.unpack('f', self.sample.read(4))
