import calendar
import datetime as dt
import struct

class Image:
    def __init__(self, ty, height, width, content):
        self.type = ty
        self.height = height
        self.width = width
        self.content = content

    def __str__(self):
        return f'{self.width}x{self.height} {self.type} image'

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.type} {self.width}x{self.height}>'


class Feelings:
    def __init__(self, hunger, thirst, exhaustion, happiness):
        self.hunger = hunger
        self.thirst = thirst
        self.exhaustion = exhaustion
        self.happiness = happiness


class Snapshot:
    def __init__(self, timestamp, translation, rotation, color_image,
                 depth_image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __str__(self):
        return f'Snapshot from {self.timestamp} on {self.translation} / {self.rotation}, ' + \
            f'with a {self.color_image} and a {self.depth_image}.'

    def with_fields(self, fields):
        timestamp = self.timestamp
        translation = (0, 0, 0)
        rotation = (0, 0, 0, 0)
        color_image = Image('color', 0, 0, [])
        depth_image = Image('depth', 0, 0, [])
        feelings = Feelings(0, 0, 0, 0)

        if 'translation' in fields:
            translation = self.translation
        if 'rotation' in fields:
            rotation = self.rotation
        if 'color_image' in fields:
            color_image = self.color_image
        if 'depth_image' in fields:
            depth_image = self.depth_image
        if 'feelings' in fields:
            feelings = self.feelings

        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)

    def serialize(self):
        msg = bytes()
        msg += struct.pack('<Q', int(1000 * self.timestamp.timestamp()))
        msg += struct.pack('ddd', *self.translation)
        msg += struct.pack('dddd', *self.rotation)
        msg += struct.pack('<II', self.color_image.width, self.color_image.height)
        msg += bytes(self.color_image.content)
        msg += struct.pack('<II', self.depth_image.width, self.depth_image.height)
        msg += bytes(self.depth_image.content)
        msg += struct.pack('ffff', self.feelings.hunger, self.feelings.thirst, \
                self.feelings.exhaustion, self.feelings.happiness)
        return msg

    @classmethod
    def deserialize(cls, data):
        timestamp = struct.unpack('<Q', data[:8])[0]
        timestamp = dt.datetime.fromtimestamp(timestamp / 1000.0)
        data = data[8:]

        translation = struct.unpack('ddd', data[:24])
        data = data[24:]

        rotation = struct.unpack('dddd', data[:32])
        data = data[32:]

        width, height = struct.unpack('<II', data[:8])
        data = data[8:]
        image_len = width * height * 3
        content = data[:image_len]
        color_image = Image('color', height, width, content)
        data = data[image_len:]

        width, height = struct.unpack('<II', data[:8])
        data = data[8:]
        image_len = width * height * 4
        content = data[:image_len]
        depth_image = Image('depth', height, width, content)
        data = data[image_len:]

        feelings = struct.unpack('ffff', data[:16])
        feelings = Feelings(*feelings)
        return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)
