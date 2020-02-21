import calendar
import datetime as dt
import struct


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def serialize(self):
        msg = bytes()
        msg += struct.pack('<Q', self.user_id)
        msg += struct.pack('<Q', calendar.timegm(self.timestamp.utctimetuple()))
        thought = self.thought.encode('utf-8')
        msg += thought
        return msg

    @classmethod
    def deserialize(cls, data):
        user_id, timestamp = struct.unpack('<QQ', data[:16])
        thought = data[16:].decode('utf-8')
        timestamp = dt.datetime.utcfromtimestamp(timestamp)

        return Thought(user_id, timestamp, thought)

    def __repr__(self):
        return f'{self.__class__.__name__}' + \
               f'(user_id={self.user_id}, ' + \
               f'timestamp={self.timestamp!r}, ' + \
               f'thought={self.thought!r})'

    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.user_id == other.user_id and \
            self.timestamp == other.timestamp and \
            self.thought == other.thought
