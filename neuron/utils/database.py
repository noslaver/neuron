from pymongo import MongoClient


class Database:
    def __init__(self, url):
        self.driver = find_driver(url)

    def create_user(self, **kwargs):
        return self.driver.create_user(**kwargs)

    def get_user(self, **kwargs):
        user = self.driver.get_user(**kwargs)
        if user is None:
            raise LookupError()
        return user

    def create_or_update_snapshot(self, user_id, snapshot_timestamp, **kwargs):
        self.driver.create_or_update_snapshot(user_id, snapshot_timestamp, **kwargs)


class MongoDriver:
    def __init__(self, url):
        self.url = url
        self.client = MongoClient(url)

    def create_user(self, user):
        users = self.client.db.users
        user = {'id': user.user_id,
                'name': user.username,
                'gender': user.gender,
                'birthday': user.birthday,
                'snapshots': []}
        users.insert_one(user)

    def get_user(self, user_id):
        users = self.client.db.users
        user = users.find_one({'id': user_id})
        return user

    def create_or_update_snapshot(self, user_id, snapshot_timestamp, ty, result):
        snapshots = self.client.db.snapshots
        snapshots.find_one_and_update({'timestamp': snapshot_timestamp},
                {'$set': {'user_id': user_id, 'timestamp': snapshot_timestamp, ty: result}},
                upsert=True)


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(url):
            return cls(url)


drivers = {'mongodb://': MongoDriver}
