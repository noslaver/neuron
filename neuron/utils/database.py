import datetime as dt
import pymongo


class Database:
    def __init__(self, url):
        self.driver = find_driver(url)

    def upsert_user(self, **kwargs):
        return self.driver.upsert_user(**kwargs)

    def get_user(self, **kwargs):
        user = self.driver.get_user(**kwargs)
        return user

    def get_users(self, **kwargs):
        users = self.driver.get_users(**kwargs)
        return users

    def get_snapshots(self, **kwargs):
        snapshots = self.driver.get_snapshots(**kwargs)
        return snapshots

    def get_snapshot(self, **kwargs):
        snapshot = self.driver.get_snapshot(**kwargs)
        return snapshot

    def get_result(self, **kwargs):
        result = self.driver.get_result(**kwargs)
        return result

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
        users.update({'id': user['id']}, user, upsert=True)

    def get_user(self, user_id):
        users = self.client.db.users
        user = users.find_one({'id': user_id}, {'_id': False})
        if user is not None:
            user['birthday'] = dt.datetime.fromtimestamp(user['birthday'])
        return user

    def get_users(self):
        users = self.client.db.users
        users = list(users.find({}, {'_id': False, 'id': True, 'name': True}))
        return users

    def get_snapshots(self, user_id):
        snapshots = self.client.db.snapshots
        snapshots = list(snapshots.find({'user_id': user_id},
                                        {'_id': False, 'timestamp': True, 'user_id': True}))
        return snapshots

    def get_snapshot(self, user_id, snapshot_id):
        snapshots = self.client.db.snapshots
        snapshot = snapshots.find_one({'user_id': user_id, 'timestamp': snapshot_id},
                                       {'_id': False})

        if snapshot is None:
            return None

        results = [res.keys() for res in snapshot['results']]
        results = [item for sublist in results for item in sublist]
        snapshot['results'] = results
        return snapshot

    def get_result(self, user_id, snapshot_id, result_name):
        snapshots = self.client.db.snapshots
        snapshot = snapshots.find_one({'user_id': user_id, 'timestamp': snapshot_id},
                                      {'_id': False, 'results': True})

        results = snapshot['results']

        result = next(filter(lambda res: result_name in res, results), None)

        if result is not None:
            return result[result_name]
        return None

    def get_data(self, user_id, snapshot_id, result_name):
        snapshots = self.client.db.snapshots
        snapshot = snapshots.find_one({'user_id': user_id, 'timestamp': snapshot_id},
                                       {'_id': False})
        return snapshot[result_name]

    def upsert_snapshot(self, user_id, snapshot_timestamp, ty, result):
        snapshots = self.client.db.snapshots
        snapshots.find_one_and_update({'timestamp': snapshot_timestamp},
                {'$set': {'user_id': user_id, 'timestamp': snapshot_timestamp}},
                upsert=True)

        result = {ty: result}
        snapshots.update({'timestamp': snapshot_timestamp}, {'$push': {'results': result}})


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(url):
            return cls(url)


drivers = {'mongodb://': MongoDriver}
