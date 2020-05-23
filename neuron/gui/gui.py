from flask import Flask, redirect, render_template, request, url_for

import json
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import requests


app = Flask(__name__)


def create_plot(user, result):
    response = requests.get(f'{app.api_url}/users/{user}/snapshots')

    if response.status_code != 200:
       return None

    snaps = json.loads(response.content)

    plot = None
    if result == 'pose':
        plot = create_pose_plot(snaps)
    if result == 'feelings':
        plot = create_feelings_plot(snaps)
    if result == 'color_image':
        plot = create_color_image_plot(snaps)
    if result == 'depth_image':
        plot = create_depth_image_plot(snaps)

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

    fig.update_layout(width=1000, height=700)

    plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot


def create_pose_plot(snaps):
    poses = []
    for snap in snaps:
        response = requests.get(
                f'{app.api_url}/users/{snap["user_id"]}/snapshots/{snap["timestamp"]}/pose')

        if response.status_code != 200:
            continue

        data = json.loads(response.content)
        data['timestamp'] = snap['timestamp']
        poses.append(data)

    t = [p['timestamp'] for p in poses]
    x = [p['translation']['x'] for p in poses]
    y = [p['translation']['y'] for p in poses]
    z = [p['translation']['z'] for p in poses]

    fig = make_subplots(rows=2, cols=1, specs=[[{'type': 'scene'}], [{'type': 'scene'}]])

    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', name='translation', marker=
        dict(size=6,
            color=t,
            colorscale='Viridis',
            opacity=0.8)),
        row=1, col=1)

    w = [p['rotation']['w'] for p in poses]
    x = [p['rotation']['x'] for p in poses]
    y = [p['rotation']['y'] for p in poses]
    z = [p['rotation']['z'] for p in poses]

    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', name='rotation', marker=
        dict(size=6,
            color=w,
            colorscale='Viridis',
            opacity=0.8)),
        row=2, col=1)

    fig.update_layout(height=700, showlegend=False)

    plot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot


def create_color_image_plot(snaps):
    images = []
    for snap in snaps:
        response = requests.get(
                f'{app.api_url}/users/{snap["user_id"]}/snapshots/{snap["timestamp"]}/color_image')

        if response.status_code != 200:
            continue

        data = json.loads(response.content)
        data['timestamp'] = snap['timestamp']
        images.append(data)

    return json.dumps(images)


def create_depth_image_plot(snaps):
    images = []
    for snap in snaps:
        response = requests.get(
                f'{app.api_url}/users/{snap["user_id"]}/snapshots/{snap["timestamp"]}/depth_image')

        if response.status_code != 200:
            continue

        data = json.loads(response.content)
        data['timestamp'] = snap['timestamp']
        images.append(data)

    return json.dumps(images)


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


@app.route('/users/<user_id>/result')
def change_features(user_id):
    result = request.args['selected']
    plot = create_plot(user_id, result)
    return plot


def run_server(host, port, api_host, api_port):
    from waitress import serve
    app.api_url = f'http://{api_host}:{api_port}'

    serve(app, host=host, port=port)
