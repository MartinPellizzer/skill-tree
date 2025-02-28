import os
import json

import pygame

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])

is_panning_begin = False

nodes = []
edges = []

'''
nodes.append({
    'id': 0,
    'x': 64*2,
    'y': 64*4,
    'w': 64*3,
    'h': 64*1,
    'text': 'ozonogroup',
    'level': '0',
    'exp': '0',
    'json_nodes_filepath': 'trees/ozonogroup/nodes.json',
    'json_edges_filepath': 'trees/ozonogroup/edges.json',
})

nodes.append({
    'id': 1,
    'x': 64*2,
    'y': 64*6,
    'w': 64*3,
    'h': 64*1,
    'text': 'terrawhisper',
    'level': '0',
    'exp': '0',
    'json_nodes_filepath': 'trees/terrawhisper/nodes.json',
    'json_edges_filepath': 'trees/terrawhisper/edges.json',
})

nodes.append({
    'id': 1,
    'x': 64*2,
    'y': 64*8,
    'w': 64*3,
    'h': 64*1,
    'text': 'martinpellizzer',
    'level': '0',
    'exp': '0',
    'json_nodes_filepath': 'trees/martinpellizzer/nodes.json',
    'json_edges_filepath': 'trees/martinpellizzer/edges.json',
})
'''

json_nodes_filepath = 'trees/nodes.json'
json_edges_filepath = 'trees/edges.json'

try: 
    with open(json_nodes_filepath) as f: nodes = json.load(f)
except: pass
try: 
    with open(json_edges_filepath) as f: edges = json.load(f)
except: pass

node_focus_index = -1
node_focus_id = -1

camera = {
    'x': 0,
    'y': 0,
    'zoom': 1,
    'x_pan_start': 0,
    'y_pan_start': 0,
}

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

dragging_node = False
dragging_node_index = -1

snapping_mode = False
control_mode = False
shift_mode = False
line_mode = False

def get_cell_hover():
    row_i = (mouse['y'] - camera['y']) // (64*camera['zoom'])
    col_i = (mouse['x'] - camera['x']) // (64*camera['zoom'])
    return row_i, col_i

font = pygame.font.SysFont('Arial', 16)

line_tmp = {
    'x_1': 0,
    'y_1': 0,
    'x_2': 0,
    'y_2': 0,
}

def draw_grid():
    for i in range(20):
        for j in range(20):
            x = (64*j + camera['x']) * camera['zoom']
            y = (64*i + camera['y']) * camera['zoom']
            w = 64*camera['zoom']
            h = 64*camera['zoom']
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)

def draw_edges():
    for edge in edges:
        node_1_id = edge['node_1_id']
        node_2_id = edge['node_2_id']
        node_1 = None
        node_2 = None
        for node in nodes:
            node_id = node['id']
            if node_id == node_1_id: node_1 = node
            elif node_id == node_2_id: node_2 = node
        x_1 = (node_1['x'] + (node_1['w'] // 2) + camera['x']) * camera['zoom']
        y_1 = (node_1['y'] + (node_1['h'] // 2) + camera['y']) * camera['zoom']
        x_2 = (node_2['x'] + (node_2['w'] // 2) + camera['x']) * camera['zoom']
        y_2 = (node_2['y'] + (node_2['h'] // 2) + camera['y']) * camera['zoom']
        pygame.draw.line(screen, '#ffffff', (x_1, y_1), (x_2, y_2))

def draw_edge_tmp():
    if line_mode == True:
        x_1 = line_tmp['x_1']
        y_1 = line_tmp['y_1']
        x_2 = mouse['x']
        y_2 = mouse['y']
        pygame.draw.line(screen, '#ffffff', (x_1, y_1), (x_2, y_2))

def draw_nodes():
    for node in nodes:
        x = (node['x'] + camera['x']) * camera['zoom']
        y = (node['y'] + camera['y']) * camera['zoom']
        w = (node['w']) * camera['zoom']
        h = (node['h']) * camera['zoom']
        pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), )
        if node['id'] == node_focus_id:
            pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h,), 1,)
        px = 8
        py = 8
        text_surface = font.render(f'{node["text"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x + px, y + py))
        px = 8
        py += 8 + 16
        text = f'EXP: {node["exp"]}'
        text_surface = font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (x + px, y + py))
        text = f'LVL: {node["level"]}'
        text_w, text_h = font.size(text)
        text_surface = font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (x + w - text_w - px, y + py))

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
    draw_grid()
    draw_edges()
    draw_edge_tmp()
    draw_nodes()
    draw_debug()
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            camera['zoom'] += event.y
            if event.y == -1:
                if camera['zoom'] < 1: 
                    camera['zoom'] = 1
                else:
                    camera['x'] *= camera['zoom']
                    camera['y'] *= camera['zoom']
            else:
                if camera['zoom'] > 8: 
                    camera['zoom'] = 8
                else:
                    camera['x'] //= camera['zoom']
                    camera['y'] //= camera['zoom']
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                j = json.dumps(nodes, indent=4)
                with open(json_nodes_filepath, 'w') as f:
                    print(j, file=f)
                j = json.dumps(edges, indent=4)
                with open(json_edges_filepath, 'w') as f:
                    print(j, file=f)
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                with open(json_nodes_filepath) as f:
                    nodes = json.load(f)
                with open(json_edges_filepath) as f:
                    edges = json.load(f)
            elif event.key == pygame.K_LALT:
                snapping_mode = True
            elif event.key == pygame.K_LCTRL:
                control_mode = True
            elif event.key == pygame.K_LSHIFT:
                shift_mode = True
            elif event.key == pygame.K_KP_MINUS:
                nodes[node_focus_index]['level'] = str(int(nodes[node_focus_index]['level']) - 1)
            elif event.key == pygame.K_KP_PLUS:
                nodes[node_focus_index]['level'] = str(int(nodes[node_focus_index]['level']) + 1)
            elif event.key == pygame.K_ESCAPE:
                with open('trees/nodes.json') as f:
                    nodes = json.load(f)
                with open('trees/edges.json') as f:
                    edges = json.load(f)
            elif event.key == pygame.K_BACKSPACE:
                if node_focus_index >= 0:
                    nodes[node_focus_index]['text'] = nodes[node_focus_index]['text'][:-1]
            else:
                _key = pygame.key.name(event.key)
                nodes[node_focus_index]['text'] += _key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LALT:
                snapping_mode = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                control_mode = False
            if event.key == pygame.K_LSHIFT:
                shift_mode = False

    screen.fill('#101010')

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

    # pan
    if pygame.mouse.get_pressed()[1] == True: # middle click
        if not is_panning_begin:
            is_panning_begin = True
            camera['x_pan_start'] = camera['x']
            camera['y_pan_start'] = camera['y']
            mouse['x_pan_start'] = mouse['x']
            mouse['y_pan_start'] = mouse['y']
        camera['x'] = camera['x_pan_start'] + (mouse['x'] - mouse['x_pan_start']) * 1//camera['zoom']
        camera['y'] = camera['y_pan_start'] + (mouse['y'] - mouse['y_pan_start']) * 1//camera['zoom']
    else:
        is_panning_begin = False

     # left click
    if pygame.mouse.get_pressed()[0] == True:
        mouse['left_click_cur'] = 1
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            for i, node in enumerate(nodes):
                x_1 = (node['x'] + camera['x']) * camera['zoom']
                y_1 = (node['y'] + camera['y']) * camera['zoom']
                x_2 = (node['x'] + node['w'] + camera['x']) * camera['zoom']
                y_2 = (node['y'] + node['h'] + camera['y']) * camera['zoom']
                if mouse['x'] >= x_1 and mouse['y'] >= y_1 and mouse['x'] < x_2 and mouse['y'] < y_2:
                    node_focus_index = i
                    node_focus_id = node['id']
                    # control click
                    if control_mode == True:
                        json_nodes_filepath = node['json_nodes_filepath']
                        json_edges_filepath = node['json_edges_filepath']
                        if not os.path.exists(json_nodes_filepath):
                            j = json.dumps([], indent=4)
                            with open(json_nodes_filepath, 'w') as f:
                                print(j, file=f)
                        if not os.path.exists(json_edges_filepath):
                            j = json.dumps([], indent=4)
                            with open(json_edges_filepath, 'w') as f:
                                print(j, file=f)
                        with open(json_nodes_filepath) as f: nodes = json.load(f)
                        with open(json_edges_filepath) as f: edges = json.load(f)
                    # drag
                    elif shift_mode == True:
                        line_tmp['x_1'] = (x_1 + x_2) // 2
                        line_tmp['y_1'] = (y_1 + y_2) // 2
                        line_mode = True
                    else:
                        node_id = node['id']
                        dragging_node = True
                        dragging_node_index = i
                        mouse['x_drag_start'] = mouse['x']
                        mouse['y_drag_start'] = mouse['y']
                        node_drag_x_start = node['x']
                        node_drag_y_start = node['y']
    else:
        mouse['left_click_cur'] = 0
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            dragging_node = False
            dragging_node_index = -1
            # drag edge e create if valid
            if line_mode == True:
                line_mode = False
                for i, node in enumerate(nodes):
                    x_1 = (node['x'] + camera['x']) * camera['zoom']
                    y_1 = (node['y'] + camera['y']) * camera['zoom']
                    x_2 = (node['x'] + node['w'] + camera['x']) * camera['zoom']
                    y_2 = (node['y'] + node['h'] + camera['y']) * camera['zoom']
                    if mouse['x'] >= x_1 and mouse['y'] >= y_1 and mouse['x'] < x_2 and mouse['y'] < y_2:
                        # check if not released on self
                        if node['id'] != node_focus_id:
                            node_1_id = node_focus_id
                            node_2_id = node['id']
                            # check if edge already exists
                            nodes_1_ids = [edge['node_1_id'] for edge in edges]
                            nodes_2_ids = [edge['node_2_id'] for edge in edges]
                            if (
                                (node_1_id in nodes_1_ids and node_2_id in nodes_2_ids) or
                                (node_2_id in nodes_1_ids and node_1_id in nodes_2_ids)
                            ):
                                pass
                            else:
                                # create
                                ids = [edge['id'] for edge in edges]
                                if ids != []:
                                    id_last = ids[-1]
                                    id_next = id_last+1
                                else:
                                    id_next = 0
                                edges.append({
                                    'id': id_next,
                                    'node_1_id': node_1_id,
                                    'node_2_id': node_2_id,
                                })
                            
        
    # add node
    if pygame.mouse.get_pressed()[2] == True: # right click
        mouse['right_click_cur'] = 1
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            ids = [node['id'] for node in nodes]
            if ids != []:
                id_last = ids[-1]
                id_next = id_last+1
            else:
                id_next = 0
            nodes.append({
                'id': id_next,
                'x': mouse['x'],
                'y': mouse['y'],
                'w': 64*3,
                'h': 64*1,
                'text': '???',
                'level': '0',
                'exp': '0',
            })
            print('click')
    else:
        mouse['right_click_cur'] = 0
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            print('release')
        
    draw_main()

pygame.quit()
