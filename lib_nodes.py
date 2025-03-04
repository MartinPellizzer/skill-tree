######################################################
# ;types
######################################################
def node_int(_id, x, y):
    node = {
        'id': _id,
        'type': 'int',
        'name': 'int',
        'x': x,
        'y': y,
        'w': 64*3,
        'h': 64*1,
        'inputs': [
        ],
        'outputs': [
            {
                'id': 0,
                'val': 0,
            },
        ],
    }
    return node

def node_add(_id):
    node = {
        'id': _id,
        'type': 'add',
        'name': 'add',
        'x': 64*10,
        'y': 64*5,
        'w': 64*3,
        'h': 64*1,
        'inputs': [
            {
                'id': 0,
                'val': 0,
            },
            {
                'id': 1,
                'val': 0,
            },
        ],
        'outputs': [
        ],
    }
    return node
