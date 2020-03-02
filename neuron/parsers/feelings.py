import json


def parse_feelings(context, snapshot):
    return dict(hunger = snapshot.feelings.hunger,
                exhaustion = snapshot.feelings.exhaustion,
                happiness = snapshot.feelings.happiness,
                thirst = snapshot.feelings.thirst)


parse_feelings.field = 'feelings'
