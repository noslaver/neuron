import datetime as dt
import importlib
import inspect
import pathlib
import sys


_DATA_DIR = 'data'


class Parsers:
    def __init__(self):
        self.parsers = {}

    def load_modules(self, root):
        root = pathlib.Path(root).absolute()
        sys.path.insert(0, str(root.parent))

        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            mod = importlib.import_module(f'{root.name}.{path.stem}',
                                          package=root.name)

            funcs = {f.field: f for name, f in mod.__dict__.items()
                     if callable(f) and name.startswith('parse')}
            self.parsers.update(funcs)

            funcs = {c.field: c().parse for name, c in mod.__dict__.items()
                     if inspect.isclass(c) and name.endswith('Parser')}
            self.parsers.update(funcs)


class ParseContext:
    def __init__(self, directory):
        self.directory = directory

    def save(self, filename, data):
        with open(self.directory / filename, 'w') as writer:
            writer.write(data)

    def path(self, filename):
        return self.directory / filename


def run_parser(parser, data):
    parsers = Parsers()
    parsers.load_modules('neuron/parsers')

    user_id = data.user_id
    date = dt.datetime.fromtimestamp(data.timestamp / 1000.0)

    directory = pathlib.Path(_DATA_DIR) / str(user_id) / date.strftime('%Y-%m-%d_%H-%M-%S-%f')
    directory.mkdir(parents=True, exist_ok=True)

    result = parsers.parsers[parser](ParseContext(directory), data)

    return {
            'data': result,
            'metadata': {
                'user_id': user_id,
                'timestamp': data.timestamp
            }}
