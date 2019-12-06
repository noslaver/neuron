import inspect
from functools import wraps
import sys

class CommandLineInterface:

    def __init__(self):
        self.functions = {}

    def command(self, f):
        self.functions[f.__name__] = f
        @wraps(f)
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        return wrapper

    def main(self):
        if len(sys.argv) < 3:
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)
        func_name = sys.argv[1]

        try:
            kwargs = dict(arg.split('=') for arg in sys.argv[2:])
        except:
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)

        if not func_name in self.functions:
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)

        f = self.functions[func_name]

        if set(inspect.getfullargspec(f).args) != kwargs.keys():
            print(f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*')
            exit(1)

        f(**kwargs)
