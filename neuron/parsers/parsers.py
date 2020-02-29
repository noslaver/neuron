from functools import wraps
import importlib
import inspect
import pathlib
import sys

class Parsers:
    def __init__(self):
        self.parsers = []

    def load_modules(self, root):
        root = pathlib.Path(root).absolute()
        sys.path.insert(0, str(root.parent))

        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            mod = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)

            funcs = [f for name, f in mod.__dict__.items() if callable(f) and name.startswith('parse')]
            self.parsers += funcs

            funcs = [c().parse for name, c in mod.__dict__.items() if inspect.isclass(c) and name.endswith('Parser')]
            self.parsers += funcs


class ParseContext:
    def __init__(self, directory):
        self.directory = directory

    def save(self, filename, data):
        with open(self.directory / filename, 'w') as writer:
            writer.write(data)

    def path(self, filename):
        return self.directory / filename
