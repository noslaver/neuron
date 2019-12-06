from datetime import datetime
import struct

class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def serialize(self):
        msg = bytes()
        msg += struct.pack('<Q', self.user_id)
        msg += struct.pack('<Q', round(int(self.timestamp.strftime('%s'))))
        thought = self.thought.encode('utf-8')
        msg += struct.pack('<I', len(thought))
        msg += thought
        return msg

    @classmethod
    def deserialize(cls, data):
        user_id, timestamp, thought_len = struct.unpack('<QQI', data[:20])
        thought = data[20:20 + thought_len].decode('utf-8')
        timestamp = datetime.fromtimestamp(timestamp)

        return Thought(user_id, timestamp, thought)

    def __repr__(self):
        return f'{self.__class__.__name__}(user_id={self.user_id}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.user_id == other.user_id and \
                self.timestamp == other.timestamp and \
                self.thought == other.thought
