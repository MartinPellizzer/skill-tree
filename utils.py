def get_socket_x(node, side, camera):
    if side == 'input': x = node['x'] + camera['x']
    elif side == 'output': x = node['x'] + node['w'] + camera['x']
    return x

def get_socket_y(node, i, camera):
    y = node['y'] + 32*i + camera['y']
    return y

