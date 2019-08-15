import json


def get_dict(str):
    return json.loads(str)


def make_json(to, msg):
    return json.dumps({'to': to, 'msg': msg})
