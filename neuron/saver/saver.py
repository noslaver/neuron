from ..utils import Database

class Saver:
    def __init__(self, db_url):
        self.database = Database(db_url)

    def save(self, parser, result):
        user_id = result.metadata.user_id
        timestamp = result.metadata.timestamp
        data = result.data
        self.database.create_or_update_snapshot(user_id, timestamp, ty=parser, result=data)
