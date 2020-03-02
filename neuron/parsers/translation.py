import json


def parse_translation(context, snapshot):
    x, y, z = snapshot.translation
    translation = json.dumps({'x': x, 'y': y, 'z': z})
    context.save('translation.json', translation)


parse_translation.field = 'translation'
