from functools import wraps
import json

class Parsers:
    parsers = {}

    @staticmethod
    def add_parser(name, parser):
        Parsers.parsers[name] = parser

    
    class ParseContext:
        def __init__(self, directory):
            self.directory = directory


    @staticmethod
    def parse_context(directory):
        return Parsers.ParseContext(directory)


def parser(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        Parsers.add_parser(name, wrapper)
        return wrapper
    return decorator


@parser('translation')
def parse_translation(context, snapshot):
    with open(context.directory / 'translation.json', 'w') as writer:
        x, y, z = snapshot.translation
        translation = {'x': x, 'y': y, 'z': z}
        json.dump(translation, writer)
