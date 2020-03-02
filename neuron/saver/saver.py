from ..utils import Database

class Saver:
    def __init__(self, db_url):
        self.database = Database(db_url)

    def save(self, parser, result):
        user = result.metadata.user

        self.database.upsert_user(user=user)

        timestamp = result.metadata.timestamp
        data = result.data
        self.database.upsert_snapshot(user.id, timestamp, ty=parser, result=data)
