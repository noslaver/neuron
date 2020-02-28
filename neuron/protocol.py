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


class Hello:
    def __init__(self, user_id, username, birthdate, gender):
        self.user_id = user_id
        self.username = username
        self.birthdate = birthdate
        self.gender = gender

    def serialize(self):
        msg = bytes()
        msg += struct.pack('<Q', self.user_id)
        msg += struct.pack('<I', len(self.username))
        username = self.username.encode('utf-8')
        msg += username
        msg += struct.pack('<I', calendar.timegm(self.birthdate.utctimetuple()))
        msg += self.gender.encode('utf-8')
        return msg

    @classmethod
    def deserialize(cls, data):
        user_id, name_len = struct.unpack('<QI', data[:12])
        data = data[12:]
        username = data[:name_len].decode('utf-8')
        data = data[name_len:]
        timestamp = struct.unpack('<I', data[:4])[0]
        birthdate = dt.datetime.utcfromtimestamp(timestamp)
        data = data[4:]
        gender = chr(data[0])

        return Hello(user_id, username, birthdate, gender)

    def __repr__(self):
        return f'{self.__class__.__name__}' + \
               f'(user_id={self.user_id}, ' + \
               f'username={self.username!r}, ' + \
               f'birthdate={self.birthdate!r}, ' + \
               f'gender={self.gender!r})'

    def __str__(self):
        return f'user {self.user_id}: {self.username}, born {self.birthdate:%B %d, %Y} ({self.gender})'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.user_id == other.user_id and \
            self.birthdate == other.birthdate and \
            self.username == other.username and \
            self.gender == other.gender


class Config:
    def __init__(self, fields):
        self.fields = fields

    def serialize(self):
        msg = bytes()
        msg += struct.pack('<I', len(self.fields))
        for field in self.fields:
            msg += struct.pack('<I', len(field))
            f = field.encode('utf-8')
            msg += f
        return msg

    @classmethod
    def deserialize(cls, data):
        fields_len = struct.unpack('<I', data[:4])[0]
        data = data[4:]
        fields = []
        for i in range(fields_len):
            field_len = struct.unpack('<I', data[:4])[0]
            data = data[4:]
            field = data[:field_len].decode('utf-8')
            data = data[field_len:]
            fields.append(field)

        return Config(fields)

    def __repr__(self):
        return f'{self.__class__.__name__}' + \
               f'(fields={self.fields!r})'

    def __str__(self):
        return f'Supported fields: {self.fields!r}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return set(self.fields) == set(other.fields)
