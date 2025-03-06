def get_socket_x(node, side, camera):
    if side == 'input': x = (node['x'] + camera['x']) * camera['zoom']
    elif side == 'output': x = (node['x'] + node['w'] + camera['x']) * camera['zoom']
    return x

def get_socket_y(node, i, camera):
    y = (node['y'] + (32*(i+1)) + camera['y']) * camera['zoom']
    return y

