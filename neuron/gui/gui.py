from flask import Flask, redirect, render_template, request, url_for

import json
import numpy as np
import plotly
import plotly.graph_objs as go
import requests


app = Flask(__name__)


def create_plot(user, result):
    response = requests.get(f'{app.api_url}/users/{user}/snapshots')

    if response.status_code != 200:
       return None

    snaps = json.loads(response.content)

    data = None
    if result == 'pose':
        data = create_pose_plot(snaps)
    if result == 'feelings':
        data = create_feelings_plot(snaps)
    if result == 'color_image':
        data = create_color_image_plot(snaps)
    if result == 'depth_image':
        data = create_depth_image_plot(snaps)

    plot = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return plot


def create_feelings_plot(snaps):
    feelings = []
    for snap in snaps:
        response = requests.get(
                f'{app.api_url}/users/{snap["user_id"]}/snapshots/{snap["timestamp"]}/feelings')

        if response.status_code != 200:
            continue

        data = json.loads(response.content)
        data['timestamp'] = snap['timestamp']
        feelings.append(data)

    x = [f['timestamp'] for f in feelings]
    y1 = [f['happiness'] for f in feelings]
    y2 = [f['thirst'] for f in feelings]
    y3 = [f['exhaustion'] for f in feelings]
    y4 = [f['hunger'] for f in feelings]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='happiness'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='thirst'))
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name='exhaustion'))
    fig.add_trace(go.Scatter(x=x, y=y4, mode='lines', name='hunger'))

    return fig


@app.route('/')
def index():
    response = requests.get(f'{app.api_url}/users')

    users = []
    if response.status_code == 200:
        users = json.loads(response.content)

    return render_template('index.html', users=users)


@app.route('/users/<user_id>')
def user(user_id):
    response = requests.get(f'{app.api_url}/users/{user_id}')

    if response.status_code != 200:
       return redirect(url_for('index'))

    user = json.loads(response.content)

    bar = create_plot(user_id, 'feelings')
    return render_template('user.html', plot=bar, user=user)


@app.route('/result')
def change_features():
    feature = request.args['selected']
    plot = create_plot(feature)
    return plot


def run_server(host, port, api_host, api_port):
    from waitress import serve
    app.api_url = f'http://{api_host}:{api_port}'

    serve(app, host=host, port=port)
