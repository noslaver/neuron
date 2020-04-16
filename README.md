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

## Usage

### Client

neuron's client allows publishing a `mind` sample to a server.
The client is availablre as both an API and a CLI.

API usage:
```python
from neuron.client import upload_sample

upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
```

CLI usage:
```bash
$ python -m neuron.client upload-sample \
        -H/--host '127.0.0.1'
        -p/--port 8000
        'snapshot.mind.gz'
```
