def get_socket_x(node, side):
    if side == 'input': x = node['x']
    elif side == 'output': x = node['x'] + node['w']
    return x

def get_socket_y(node, i=0):
    y = node['y'] + 32*i
    return y

