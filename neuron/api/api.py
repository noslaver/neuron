from ..utils import Database
from flask import Flask, g, jsonify, request


app = Flask(__name__)
db = None


@app.route('/users', methods=['GET'])
def users():
    users = db.get_users()
    return jsonify(users)


@app.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    user = db.get_user(user_id=user_id)
    return jsonify(user)


@app.route('/users/<user_id>/snapshots', methods=['GET'])
def snapshots(user_id):
    snapshots = db.get_snapshots(user_id=user_id)
    return jsonify(snapshots)


@app.route('/users/<user_id>/snapshots/<int:snapshot_id>', methods=['GET'])
def snapshot(user_id, snapshot_id):
    snapshot = db.get_snapshot(user_id=user_id, snapshot_id=snapshot_id)
    return jsonify(snapshot)


@app.route('/users/<user_id>/snapshots/<int:snapshot_id>/<result_name>', methods=['GET'])
def result(user_id, snapshot_id, result_name):
    result = db.get_result(user_id=user_id, snapshot_id=snapshot_id, result_name=result_name)
    return jsonify(result)


@app.route('/users/<user_id>/snapshots/<int:snapshot_id>/<result_name>/data', methods=['GET'])
def result_data(user_id, snapshot_id, result_name):
    data_path = db.get_result(user_id, snapshot_id, result_name)
    return send_file(data_path)


def run_api_server(host, port, db_url):
    global db
    db = Database(db_url)

    app.run(host=host, port=port)
