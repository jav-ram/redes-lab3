import json


def get_dict(str):
    return json.loads(str)


def make_msg_json(origin, me, to, msg, hops=0, distance=0):
    return json.dumps({
        'type': 'message',
        'origin': origin,
        'from': me,
        'to': to,
        'hops': hops,
        'distance': distance,
        'msg': msg,
    })


def make_neighbors_list(me, table):

    return json.dumps({
        'type': 'connection',
        'from': me,
        'table': table,
    })


def make_connection_json(me, distance):
    return json.dumps({
        'type': 'connection',
        'from': me,
        'distance': distance,
    })


def make_response_json(me, neighbors):
    return json.dumps({
        'type': 'response',
        'from': me,
        'distance': distance,
    })
