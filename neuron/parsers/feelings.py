import json


def parse_feelings(context, snapshot):
    context.save('feelings.json', json.dumps(snapshot.feelings.__dict__))

parse_feelings.field = 'feelings'
