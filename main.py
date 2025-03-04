import os
import json

import pygame

import lib_nodes

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])

nodes = []
edges = []

nodes.append(lib_nodes.node_int(_id=0, x=64*5, y=64*5))
nodes.append(lib_nodes.node_int(_id=1, x=64*5, y=64*7))
nodes.append(lib_nodes.node_add(_id=2))

edge_0 = {
    'id': 0,
    'input': {
        'node_id': 2,
        'socket_id': 0,
    },
    'output': {
        'node_id': 0,
        'socket_id': 0,
    },
}

edge_1 = {
    'id': 0,
    'input': {
        'node_id': 2,
        'socket_id': 1,
    },
    'output': {
        'node_id': 1,
        'socket_id': 0,
    },
}

edges.append(edge_0)
edges.append(edge_1)

font = pygame.font.SysFont('Arial', 16)

def get_socket_x(node, side):
    if side == 'input': x = node['x']
    elif side == 'output': x = node['x'] + node['w']
    return x

def get_socket_y(node, i=0):
    y = node['y'] + 32*i
    return y

def get_edges_in(node):
    global edges
    edges_filtered = []
    for edge in edges:
        node_inputs_ids = [item['id'] for item in node['inputs']]
        if edge['input_id'] in node_inputs_ids:
            edges_filtered.append(edge)
    return edges_filtered

def updates_nodes():
    global nodes
    global edges
    for node_cur in nodes:
        if node_cur['type'] == 'read':
            # has edge
            edges = get_edges_in(node_cur)
            if edges == []: continue

            edge_1 = edges[0]
            edge_2 = edges[1]

            res = 0
            edge_output_id = edge_1['output_id']
            # get other side of edge
            print(edge_output_id)
            for node_check in nodes:
                if node_check['outputs'] != []:
                   if node_check['outputs'][0]['id'] == edge_output_id:
                        socket_other_val = node_check['outputs'][0]['val']
                        res += socket_other_val
                        node_cur['inputs'][0]['val'] = socket_other_val

            edge_output_id = edge_2['output_id']
            # get other side of edge
            print(edge_output_id)
            for node_check in nodes:
                if node_check['outputs'] != []:
                   if node_check['outputs'][0]['id'] == edge_output_id:
                        socket_other_val = node_check['outputs'][0]['val']
                        res += socket_other_val
                        node_cur['inputs'][1]['val'] = socket_other_val

            node_cur['name'] = res

def draw_nodes():
    for node in nodes:
        x = node['x']
        y = node['y']
        w = node['w']
        h = node['h']
        pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
        text_surface = font.render(f'{node["name"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x + 64, y + 16))
        for i, socket in enumerate(node['inputs']):
            x = get_socket_x(node, 'input')
            y = get_socket_y(node, i)
            pygame.draw.circle(screen, '#ffffff', (x, y), 10)
            text_surface = font.render(f'{socket["val"]}', False, (255, 255, 255))
            screen.blit(text_surface, (x + 16, y + 16))
        for i, socket in enumerate(node['outputs']):
            x = get_socket_x(node, 'output')
            y = get_socket_y(node, i)
            pygame.draw.circle(screen, '#ffffff', (x, y), 10)
            text_surface = font.render(f'{socket["val"]}', False, (255, 255, 255))
            screen.blit(text_surface, (x + 16, y + 16))

def draw_edges_old():
    for edge in edges:
        x1 = -1
        y1 = -1
        x2 = -1
        y2 = -1
        for node in nodes:
            inputs_ids = [item['id'] for item in node['inputs']]
            outputs_ids = [item['id'] for item in node['outputs']]
            for i, socket in enumerate(node['inputs']):
                if edge['input_id'] == socket['id']:
                    x1 = get_socket_x(node, 'input')
                    y1 = get_socket_y(node, i)
            for i, socket in enumerate(node['outputs']):
                if edge['output_id'] == socket['id']:
                    x2 = get_socket_x(node, 'output')
                    y2 = get_socket_y(node, i)
        if x1 != -1 and y1 != -1 and x2 != -1 and y2 != -1:
            pygame.draw.line(screen, '#ffffff', (x1, y1), (x2, y2))

def draw_edges():
    for edge in edges:
        x1 = -1
        y1 = -1
        x2 = -1
        y2 = -1
        for node in nodes:
            if edge['input']['node_id'] == node['id']:
                # print(edge['input']['node_id'], node['id'])
                for i, socket in enumerate(node['inputs']):
                    if edge['input']['socket_id'] == socket['id']:
                        # print(edge['input']['socket_id'], socket['id'])
                        x1 = get_socket_x(node, 'input')
                        y1 = get_socket_y(node, i)
            if edge['output']['node_id'] == node['id']:
                for i, socket in enumerate(node['outputs']):
                    if edge['output']['socket_id'] == socket['id']:
                        # print(edge['output']['socket_id'], socket['id'])
                        x2 = get_socket_x(node, 'output')
                        y2 = get_socket_y(node, i)
        if x1 != -1 and y1 != -1 and x2 != -1 and y2 != -1:
            pygame.draw.line(screen, '#ffffff', (x1, y1), (x2, y2))

def draw_debug():
    y = 24
    text_surface = font.render(f'x: {mouse["x"]} - y: {mouse["y"]}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24
    row_i, col_i = get_cell_hover()
    text_surface = font.render(f'row: {row_i} - col: {col_i}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24
    text_surface = font.render(f'camera_x: {camera["x"]} - camera_y: {camera["y"]}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24
    text_surface = font.render(f'camera_zoom: {camera["zoom"]}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24
    text_surface = font.render(f'snapping_mode: {snapping_mode}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24
    text_surface = font.render(f'shift_mode: {shift_mode}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24
    text_surface = font.render(f'edges_num: {len(edges)}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24

def draw_main():
    # draw_grid()
    # draw_edges()
    # draw_edge_tmp()
    # draw_debug()

    draw_nodes()
    draw_edges()

   
    pygame.display.flip()

def node_create():
    x, y = world_coords()
    w = 64*3
    h = 64*1
    
    node = {
        'id': 0,
        'type': 'add',
        'x': x,
        'y': y,
        'w': 64*3,
        'h': 64*1,
        'text': 'skill 1',
        'inputs': [
            {
                'id': 0,
                'type': 'int',
                'val': 0,
            },
            {
                'id': 1,
                'type': 'int',
                'val': 0,
            },
        ],
        'outputs': [
            {
                'id': 0,
                'type': 'int',
                'val': 0,
            },
        ],
    }
    nodes_new.append(node)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('#101010')

    '''
    # inputs/update
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()

    # drag
    if dragging_node == True:
        # TODO: bugged a bit (when moving mouse doesn't snap a bit of mouse hovered cell on zoom 2) 
        if snapping_mode == True:
            row_i, col_i = get_cell_hover()
            nodes[dragging_node_index]['x'] = col_i*64
            nodes[dragging_node_index]['y'] = row_i*64
        else:
            nodes[dragging_node_index]['x'] = node_drag_x_start + (mouse['x'] - mouse['x_drag_start']) * 1//camera['zoom']
            nodes[dragging_node_index]['y'] = node_drag_y_start + (mouse['y'] - mouse['y_drag_start']) * 1//camera['zoom']
    '''

    # pan
    # camera_pan()

    # mouse_main()
        
    # updates_nodes()
    draw_main()

pygame.quit()
