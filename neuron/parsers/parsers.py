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


def parse(parser, data):
    parsers = Parsers()
    parsers.load_modules('neuron/parsers')

    user = data.user
    date = dt.datetime.fromtimestamp(data.timestamp / 1000.0)

    directory = pathlib.Path(_DATA_DIR) / str(user.id) / date.strftime('%Y-%m-%d_%H-%M-%S-%f')
    directory.mkdir(parents=True, exist_ok=True)

    result = parsers.parsers[parser](ParseContext(directory), data)

    return {
            'data': result,
            'metadata': {
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'birthday': user.birthday,
                    'gender': user.gender
                },
                'timestamp': data.timestamp
            }}
