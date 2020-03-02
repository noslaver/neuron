import pymongo


class Database:
    def __init__(self, url):
        self.driver = find_driver(url)

    def upsert_user(self, **kwargs):
        return self.driver.upsert_user(**kwargs)

    def get_user(self, **kwargs):
        user = self.driver.get_user(**kwargs)
        if user is None:
            raise LookupError()
        return user

    def upsert_snapshot(self, user_id, snapshot_timestamp, **kwargs):
        self.driver.upsert_snapshot(user_id, snapshot_timestamp, **kwargs)


class MongoDriver:
    def __init__(self, url):
        self.url = url
        self.client = pymongo.MongoClient(url)

        db = self.client.db

        db.users.create_index([('id', pymongo.ASCENDING)],unique=True)
        db.snapshots.create_index([('timestamp', pymongo.ASCENDING)],unique=True)

    def upsert_user(self, user):
        users = self.client.db.users
        user_to_insert = {'id': user.id,
                          'name': user.name,
                          'gender': user.gender,
                          'birthday': user.birthday}
        users.update({'id': user.id}, user_to_insert, upsert=True)

    def get_user(self, user_id):
        users = self.client.db.users
        user = users.find_one({'id': user_id})
        return user

    def upsert_snapshot(self, user_id, snapshot_timestamp, ty, result):
        snapshots = self.client.db.snapshots
        # TODO - result isn't saved correctly (fields aren't named)
        snapshots.find_one_and_update({'timestamp': snapshot_timestamp},
                {'$set': {'user_id': user_id, 'timestamp': snapshot_timestamp, ty: result}},
                upsert=True)


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(url):
            return cls(url)


drivers = {'mongodb://': MongoDriver}
