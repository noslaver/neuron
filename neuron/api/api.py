from flask import Flask, request


app = Flask(__name__)


@app.route('/users', methods=['GET'])
def users():
    return ('', 204)


@app.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    return ('', 204)


@app.route('/users/<user_id>/snapshots', methods=['GET'])
def snapshots(user_id):
    return ('', 204)


@app.route('/users/<user_id>/snapshots/<snapshot_id>', methods=['GET'])
def snapshot(user_id, snapshot_id):
    return ('', 204)


@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>', methods=['GET'])
def result(user_id, snapshot_id, result_name):
    return ('', 204)


@app.route('/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data', methods=['GET'])
def result_data(user_id, snapshot_id, result_name):
    return ('', 204)


def run_server(host, port, publish):
    app.run(host=host, port=port)
