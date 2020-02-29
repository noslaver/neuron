import datetime as dt
import struct

from .protocol import Image, Feelings, Snapshot


class BinaryParser:
    def parse_user_info(self, fp):
        user_id = self.read_long(fp)

        name_len = self.read_int(fp)
        username = fp.read(name_len).decode('utf-8')

        birthdate = dt.datetime.fromtimestamp(self.read_int(fp))

        gender = fp.read(1).decode('utf-8')

        return (user_id, username, birthdate, gender)

    def parse_snapshot(self, fp):
        timestamp = dt.datetime.fromtimestamp(self.read_long(fp) / 1000.0)

        x = self.read_double(fp)
        y = self.read_double(fp)
        z = self.read_double(fp)
        translation = (x, y, z)

        x = self.read_double(fp)
        y = self.read_double(fp)
        z = self.read_double(fp)
        w = self.read_double(fp)
        rotation = (x, y, z, w)

        height = self.read_int(fp)
        width = self.read_int(fp)
        # TODO - convert BGR to RGB
        image_pixels = fp.read(height * width * 3)
        color_image = Image('color', height, width, image_pixels)

        height = self.read_int(fp)
        width = self.read_int(fp)
        image_depths = fp.read(height * width * 4)
        depth_image = Image('depth', height, width, image_depths)

        hunger = self.read_float(fp)
        thirst = self.read_float(fp)
        exhaustion = self.read_float(fp)
        happiness = self.read_float(fp)
        feelings = Feelings(hunger, thirst, exhaustion, happiness)

        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)

    def read_int(self, fp):
        return int.from_bytes(fp.read(4), 'little')

    def read_long(self, fp):
        return int.from_bytes(fp.read(8), 'little')

    def read_double(self, fp):
        return struct.unpack('d', fp.read(8))[0]

    def read_float(self, fp):
        return struct.unpack('f', fp.read(4))[0]


class Reader:
    def __init__(self, path, parser=BinaryParser()):
        self.path = path
        self.fp = open(path, 'rb')
        self.parser = parser

    def read_user_info(self):
        try:
            (self.user_id, self.username, self.birthdate, self.gender) = self.parser.parse_user_info(self.fp)
        except Exception as e:
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
