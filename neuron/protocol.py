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
        return f'<{self.__class__.__name__}: {self.type} \
            {self.width}x{self.height}>'


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
        return f'Snapshot from {self.timestamp} on {self.translation} / {self.rotation}, \
            with a {self.color_image} and a {self.depth_image}.'


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
