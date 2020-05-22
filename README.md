[![Build Status](https://travis-ci.org/noslaver/neuron.svg?branch=master)](https://travis-ci.org/noslaver/neuron)
[![codecov](https://codecov.io/gh/noslaver/neuron/branch/master/graph/badge.svg)](https://codecov.io/gh/noslaver/neuron)

# neuron
A python Brain-Computer interface

## Installation

1. Clone the repository and enter it:

```sh
$ git clone git@github:noslaver/neuron.git
...
$ cd neuron/
```

2. Run the installation script and activate the virtual environment:

```sh
$ ./scripts/install.sh
...
$ source .env/bin/activate
[neuron] $ # you're good to go!
```

3. To check that everything is working as expected, run the tests:

```sh
$ pytest tests
...
```

## Deployment
neuron can be fully deployed in a docker environment, using the `run-pipeline.sh` script.

## Usage

### Client

neuron's client allows publishing a `mind` sample to a server.
The client is available as both an API and a CLI.

API usage:
```python
from neuron.client import upload_sample

upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
```

CLI usage:
```bash
$ python -m neuron.client upload-sample \
        -H/--host '127.0.0.1' \
        -p/--port 8000 \
        'snapshot.mind.gz'
```

### Server

neuron's server receives `mind` samples uploaded by clients and publishes them.
Clients should send a `POST` request to `/users/<user_id>/snapshots`. The request body should contain a Protobuf message of type SnapshotInfo, as described in `neuron/protobuf/neuron.proto`.
The exact publish method is configurable. By default, received samples are published to a RabbitMQ message bus.

Note that large binary data is saved to local storage, and only its location is published.

The server is available as both an API and a CLI.

API usage:
```python
from neuron.server import run_server

def handle_sample(sample):
    print(sample)

upload_sample(host='127.0.0.1', port=8000, publish=handle_sample)
```

CLI usage:
```bash
$ python -m neuron.client run-server \
        -H/--host '127.0.0.1' \
        -p/--port 8000 \
        'rabbitmq://127.0.0.1:5672'
```

### Parsers

neuron's parsers process incoming `mind` samples. Each parser specifies which part of the sample it is interested and returns a processed result, which based on the interface used, can be published to a message queue or output to sdtout.

API usage:
```python
from cortex.parsers import parse
data = ...
result = parse('pose', data)
```

CLI usage:
There are two usage, one to parse a file containig raw data:
```bash
$ python -m cortex.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```

The other subscribes to a message queue and publishes the processed result back to the broker:
```bash
$ python -m cortex.parsers run_parser 'pose' 'rabbitmq://127.0.0.1:5672'
```

#### Adding a new parser

To add a new parsers, simply add a new `.py` file into `neuron/parsers`. You can expose your parser either with a class or with a function.
To expose as a class, your file should contain a class whose name ends with "Parser". The class should have a `parse(self, context, snapshot)` method.
The class should also have a attribute named `field` which is a string indicating which parts of the snapshot it should be passed (e.g. `pose`).

To expose as a function, your file should contain a function whose name begins with "parse".
The function signature should be `parse_xxx(context, snapshot)`.
You should add an attribute to the function named `field` which is a string indicating which parts of the snapshot it should be passed (e.g. `pose`).

### Saver

neuron's saver allows saving processed `mind` data, published by the parsers, into databases.

API usage:
```python
from cortex.saver import Saver
saver = Saver(database_url)
data = ...
saver.save('pose', data)
```

CLI usage:
There are two usage, one to save a file containig processed data:
```bash
$ python -m cortex.saver save \
    -d/--database 'mongodb://127.0.0.1:27017' \
    'pose' \
    'pose.result'
```

The other subscribes to a message queue and saves published processed data to the database:
```bash
$ python -m cortex.saver run_saver \
    'mongodb://127.0.0.1:27017' \
    'rabbitmq://127.0.0.1:5672'
```

### API

neuron's API allows a runs a server which exposes the processed data to an endpoint user via HTTP.

API usage:
```python
from cortex.api import run_api_server
run_api_server(
    host = '127.0.0.1',
    port = 8000,
    database_url = 'mongodb://127.0.0.1:27017' 
)
```

CLI usage:
```bash
$ python -m cortex.api run-server \
    -H/--host '127.0.0.1' \
    -p/--port 8000 \
    -d/--database 'mongodb://127.0.0.1:27017'
```

The API exposes the following endpoints:
* **GET /users**

    Returns the list of all the supported users.

* **GET /user/{user_id}**

    Returns the specified user's info.

* **GET /user/{user_id}/snapshots**

    Returns the list of the specified user's snapshots.

* **GET /user/{user_id}/snapshots/{snapshot_id}**

    Returns the specified snapshot's info.
    Note that a snapshot is identified by its timestamp.

* **GET /user/{user_id}/snapshots/{snapshot_id}/{results-name}**

    Returns the specified snapshot's result.

### CLI

neuron's CLI consumes neuron's API.

CLI usage:
```bash
$ python -m cortex.cli get-users

$ python -m cortex.cli get-user 42

$ python -m cortex.cli get-snapshot 42 1575446890088

$ python -m cortex.cli get-snapshot 42 1575446890088 pose
```

### GUI
