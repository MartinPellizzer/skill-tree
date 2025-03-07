import os
import json

import pygame

import lib_nodes
import utils

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])

nodes_filepath_cur = ''
edges_filepath_cur = ''

mouse = {
    'x': 0,
    'y': 0,
    'x_drag_start': 0,
    'y_drag_start': 0,
    'x_pan_start': 0,
    'y_pan_start': 0,
    'left_click_old': 0,
    'left_click_cur': 0,
    'middle_click_old': 0,
    'middle_click_cur': 0,
    'right_click_old': 0,
    'right_click_cur': 0,
}

camera = {
    'x': 0,
    'y': 0,
    'zoom': 1,
    'camera_x_start': 0,
    'camera_y_start': 0,
}

drag = {
    'state': False,
    'node_index': -1,
    'node_x_start': -1,
    'node_y_start': -1,
}

pan = {
    'state': False,
}

node_focus_index = -1

nodes = []
edges = []

def load_nodes():
    global nodes
    with open(nodes_filepath_cur) as f:
        nodes = json.load(f)

def load_edges():
    global edges
    with open(edges_filepath_cur) as f:
        edges = json.load(f)

def save_nodes():
    global nodes
    j = json.dumps(nodes, indent=4)
    with open(nodes_filepath_cur, 'w') as f:
        print(j, file=f)

def save_edges():
    global edges
    j = json.dumps(edges, indent=4)
    with open(edges_filepath_cur, 'w') as f:
        print(j, file=f)

def test_data_init():
    global nodes
    global edges
    nodes.append(lib_nodes.node_skill_start(_id=3, name='ART_PLANTS', x=64*4, y=64*5))
    nodes.append(lib_nodes.node_skill(_id=4, name='LV1: TEXT', x=64*8, y=64*5))
    nodes.append(lib_nodes.node_skill(_id=5, name='LV2: LINKS', x=64*12, y=64*5))
    nodes.append(lib_nodes.node_skill(_id=6, name='LV3: IMAGES', x=64*18, y=64*5))
    nodes.append(lib_nodes.node_skill(_id=7, name='LV4: STUDIES', x=64*22, y=64*5))

    nodes.append(lib_nodes.node_skill(_id=8, name='LV0: ART_PLANT', x=64*8, y=64*8))
    nodes.append(lib_nodes.node_skill(_id=9, name='LV1: TEXT', x=64*12, y=64*8))

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

    # edges.append(edge_0)
    # edges.append(edge_1)

    edges.append({
        'id': 2,
        'input': {
            'node_id': 4,
            'socket_id': 0,
        },
        'output': {
            'node_id': 3,
            'socket_id': 0,
        },
    })

    edges.append({
        'id': 3,
        'input': {
            'node_id': 5,
            'socket_id': 0,
        },
        'output': {
            'node_id': 4,
            'socket_id': 0,
        },
    })

    edges.append({
        'id': 4,
        'input': {
            'node_id': 8,
            'socket_id': 0,
        },
        'output': {
            'node_id': 5,
            'socket_id': 0,
        },
    })

    edges.append({
        'id': 5,
        'input': {
            'node_id': 9,
            'socket_id': 0,
        },
        'output': {
            'node_id': 8,
            'socket_id': 0,
        },
    })

    edges.append({
        'id': 6,
        'input': {
            'node_id': 6,
            'socket_id': 0,
        },
        'output': {
            'node_id': 8,
            'socket_id': 0,
        },
    })

# test_data_init()

font = pygame.font.SysFont('Arial', 16)

def get_edges_in(node):
    global edges
    edges_filtered = []
    for edge in edges:
        # node_inputs_ids = [item['id'] for item in node['inputs']]
        # if edge['input']['node_id'] in node_inputs_ids:
            # edges_filtered.append(edge)
        if edge['input']['node_id'] == node['id']:
            edges_filtered.append(edge)
    return edges_filtered

def get_socket_out_of_edge(edge):
    global nodes
    socket = {}
    for node in nodes:
        if edge['output']['node_id'] == node['id']:
            found = False
            for output in node['outputs']:
                if edge['output']['socket_id'] == output['id']:
                    socket = output
                    found = True
                    break
            if found:
                break
    return socket

################################################################
# update
################################################################
def update_node_skill():
    pass

def update_nodes():
    '''
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
    '''
    for node in nodes:
        if node['type'] == 'skill':
            edges = get_edges_in(node)
            if edges == []: continue
            edge = edges[0]

            socket_other = get_socket_out_of_edge(edge)
            socket_other_val = socket_other['val']

            node['inputs'][0]['val'] = socket_other_val
            if node['inputs'][0]['val'] > 0:
                node['background_color'] = '#303030'
            else:
                node['background_color'] = '#000000'

            if node['inputs'][0]['val'] > 0 and node['outputs'][0]['val'] == 0:
                node['outline_color'] = '#fb923c'
            else:
                node['outline_color'] = '#303030'

################################################################
# draw
################################################################
def draw_node_name(text, x, y):
    text_surface = font.render(text, False, (255, 255, 255))
    screen.blit(text_surface, (x + 16, y + 16))

def draw_socket_val(text, x, y):
    text_surface = font.render(text, False, (255, 255, 255))
    screen.blit(text_surface, (x + 16, y + 16))

def draw_nodes():
    socket_r = 10 * camera['zoom']
    for i, node in enumerate(nodes):
        x = (node['x'] + camera['x']) * camera['zoom']
        y = (node['y'] + camera['y']) * camera['zoom']
        w = (node['w'] * camera['zoom'])
        h = (node['h'] * camera['zoom'])
        pygame.draw.rect(screen, node['background_color'], pygame.Rect(x, y, w, h))
        pygame.draw.rect(screen, node['outline_color'], pygame.Rect(x, y, w, h), 1)
        if i == node_focus_index:
            pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
        draw_node_name(f'{node["name"]}', x, y)
        for i, socket in enumerate(node['inputs']):
            x = utils.get_socket_x(node, 'input', camera)
            y = utils.get_socket_y(node, i, camera)
            pygame.draw.circle(screen, '#ffffff', (x, y), socket_r)
            draw_socket_val(f'{socket["val"]}', x, y)
        for i, socket in enumerate(node['outputs']):
            x = utils.get_socket_x(node, 'output', camera)
            y = utils.get_socket_y(node, i, camera)
            pygame.draw.circle(screen, '#ffffff', (x, y), socket_r)
            draw_socket_val(f'{socket["val"]}', x, y)

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
                        x1 = utils.get_socket_x(node, 'input', camera)
                        y1 = utils.get_socket_y(node, i, camera)
            if edge['output']['node_id'] == node['id']:
                for i, socket in enumerate(node['outputs']):
                    if edge['output']['socket_id'] == socket['id']:
                        # print(edge['output']['socket_id'], socket['id'])
                        x2 = utils.get_socket_x(node, 'output', camera)
                        y2 = utils.get_socket_y(node, i, camera)
        if x1 != -1 and y1 != -1 and x2 != -1 and y2 != -1:
            pygame.draw.line(screen, '#ffffff', (x1, y1), (x2, y2), camera['zoom'])

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

################################################
# camera
################################################
def camera_pan():
    if pan['state'] == True:
        camera['x'] = pan['camera_x_start'] + (mouse['x'] - mouse['x_pan_start']) // camera['zoom']
        camera['y'] = pan['camera_y_start'] + (mouse['y'] - mouse['y_pan_start']) // camera['zoom']

################################################
# mouse
################################################
def get_clicked_node_index():
    index = -1
    for i, node in enumerate(nodes):
        x_1 = node['x'] + camera['x']
        y_1 = node['y'] + camera['y']
        x_2 = node['x'] + camera['x'] + node['w']
        y_2 = node['y'] + camera['y'] + node['h']
        if mouse['x'] >= x_1 and mouse['y'] >= y_1 and mouse['x'] < x_2 and mouse['y'] < y_2:
            index = i
            break
    return index

def mouse_drag_node():
    global drag
    if drag['state'] == True:
        nodes[drag['node_index']]['x'] = drag['node_x_start'] + (mouse['x'] - mouse['x_drag_start'])
        nodes[drag['node_index']]['y'] = drag['node_y_start'] + (mouse['y'] - mouse['y_drag_start'])

def mouse_left():
    global node_focus_index
    global drag
    mouse_left_press = pygame.mouse.get_pressed()[0]
    if mouse_left_press == True:
        mouse['left_click_cur'] = 1
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            print('left click')
            # selected node to drag?
            node_focus_index = get_clicked_node_index()
            if node_focus_index != -1:
                drag['state'] = True
                drag['node_index'] = node_focus_index
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

def mouse_middle():
    mouse_left_press = pygame.mouse.get_pressed()[1]
    if mouse_left_press == True:
        mouse['middle_click_cur'] = 1
        if mouse['middle_click_old'] != mouse['middle_click_cur']:
            mouse['middle_click_old'] = mouse['middle_click_cur']
            print('middle click')
            pan['state'] = True
            mouse['x_pan_start'] = mouse['x']
            mouse['y_pan_start'] = mouse['y']
            pan['camera_x_start'] = camera['x']
            pan['camera_y_start'] = camera['y']
    else:
        mouse['middle_click_cur'] = 0
        if mouse['middle_click_old'] != mouse['middle_click_cur']:
            mouse['middle_click_old'] = mouse['middle_click_cur']
            print('middle release')
            pan['state'] = False

def mouse_main():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    mouse_left()
    mouse_middle()
    
################################################
# managers
################################################
def manage_inputs():
    global running
    global nodes_filepath_cur
    global edges_filepath_cur
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_KP_MINUS:
                if nodes[node_focus_index]['outputs'][0]['val'] > 0:
                    nodes[node_focus_index]['outputs'][0]['val'] -= 1
            elif event.key == pygame.K_KP_PLUS:
                if len(nodes[node_focus_index]['inputs']) > 0:
                    if nodes[node_focus_index]['inputs'][0]['val'] != 0:
                        if nodes[node_focus_index]['outputs'][0]['val'] < 10:
                            nodes[node_focus_index]['outputs'][0]['val'] += 1
                else:
                    if nodes[node_focus_index]['outputs'][0]['val'] < 10:
                        nodes[node_focus_index]['outputs'][0]['val'] += 1
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_nodes()
                save_edges()
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                nodes_filepath_cur = 'nodes.json'
                edges_filepath_cur = 'edges.json'
                load_nodes()
                load_edges()
        if event.type == pygame.MOUSEWHEEL:
            camera['zoom'] += event.y
            if event.y == -1:
                if camera['zoom'] < 1: camera['zoom'] = 1
            else:
                if camera['zoom'] > 8: camera['zoom'] = 8
    mouse_main()

def manage_update():
    mouse_drag_node()
    camera_pan()
    update_nodes()

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
