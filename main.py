import os
import json

import pygame

import lib_nodes
import utils

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])

mouse = {
    'x': 0,
    'y': 0,
    'x_drag_start': 0,
    'y_drag_start': 0,
    'x_pan_start': 0,
    'y_pan_start': 0,
    'left_click_old': 0,
    'left_click_cur': 0,
    'right_click_old': 0,
    'right_click_cur': 0,
}

drag = {
    'state': False,
    'node_index': -1,
    'node_x_start': -1,
    'node_y_start': -1,
}


'''
node_focus_index = -1
node_focus_id = -1
'''

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
            x = utils.get_socket_x(node, 'input')
            y = utils.get_socket_y(node, i)
            pygame.draw.circle(screen, '#ffffff', (x, y), 10)
            text_surface = font.render(f'{socket["val"]}', False, (255, 255, 255))
            screen.blit(text_surface, (x + 16, y + 16))
        for i, socket in enumerate(node['outputs']):
            x = utils.get_socket_x(node, 'output')
            y = utils.get_socket_y(node, i)
            pygame.draw.circle(screen, '#ffffff', (x, y), 10)
            text_surface = font.render(f'{socket["val"]}', False, (255, 255, 255))
            screen.blit(text_surface, (x + 16, y + 16))

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
                        x1 = utils.get_socket_x(node, 'input')
                        y1 = utils.get_socket_y(node, i)
            if edge['output']['node_id'] == node['id']:
                for i, socket in enumerate(node['outputs']):
                    if edge['output']['socket_id'] == socket['id']:
                        # print(edge['output']['socket_id'], socket['id'])
                        x2 = utils.get_socket_x(node, 'output')
                        y2 = utils.get_socket_y(node, i)
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

def get_clicked_node_index():
    node_index = -1
    for i, node in enumerate(nodes):
        x_1 = node['x']
        y_1 = node['y']
        x_2 = node['x'] + node['w']
        y_2 = node['y'] + node['h']
        if mouse['x'] >= x_1 and mouse['y'] >= y_1 and mouse['x'] < x_2 and mouse['y'] < y_2:
            node_index = i
            break
    return node_index

################################################
# mouse
################################################
def mouse_drag_node():
    global drag
    if drag['state'] == True:
        nodes[drag['node_index']]['x'] = drag['node_x_start'] + (mouse['x'] - mouse['x_drag_start'])
        nodes[drag['node_index']]['y'] = drag['node_y_start'] + (mouse['y'] - mouse['y_drag_start'])

def mouse_left():
    global drag
    mouse_left_press = pygame.mouse.get_pressed()[0]
    if mouse_left_press == True:
        mouse['left_click_cur'] = 1
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            print('left click')
            # selected node to drag?
            node_index = get_clicked_node_index()
            if node_index != -1:
                drag['state'] = True
                drag['node_index'] = node_index
                mouse['x_drag_start'] = mouse['x']
                mouse['y_drag_start'] = mouse['y']
                drag['node_x_start'] = nodes[drag['node_index']]['x']
                drag['node_y_start'] = nodes[drag['node_index']]['y']
    else:
        mouse['left_click_cur'] = 0
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            print('left release')
            drag['state'] = False
            drag['node_index'] = -1

def mouse_main():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    mouse_left()
    
################################################
# managers
################################################
def manage_inputs():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse_main()

def manage_update():
    mouse_drag_node()
    # camera_pan()

def manage_draw():
    screen.fill('#101010')
    draw_nodes()
    draw_edges()
    pygame.display.flip()

################################################
# main
################################################
running = True
while running:
    manage_inputs()
    manage_update()
    manage_draw()

pygame.quit()
