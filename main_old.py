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

node_focus_index = -1
node_focus_id = -1

is_panning_begin = False

json_nodes_filepath = 'trees/nodes.json'
json_edges_filepath = 'trees/edges.json'

try: 
    with open(json_nodes_filepath) as f: nodes = json.load(f)
except: pass
try: 
    with open(json_edges_filepath) as f: edges = json.load(f)
except: pass

def drag_node(node, i):
    node_id = node['id']
    dragging_node = True
    dragging_node_index = i
    mouse['x_drag_start'] = mouse['x']
    mouse['y_drag_start'] = mouse['y']
    node_drag_x_start = node['x']
    node_drag_y_start = node['y']

def init_edge_old():
    line_tmp['x_1'] = (x_1 + x_2) // 2
    line_tmp['y_1'] = (y_1 + y_2) // 2
    line_mode = True

def mouse_left():
    global line_mode
    mouse_left_press = pygame.mouse.get_pressed()[0]
    if mouse_left_press == True:
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
                    if control_mode == True:
                        open_tree()
                    if shift_mode == True:
                        init_edge_old()
                    else:
                        drag_node(node, i)
            
            init_edge_tmp()
    else:
        mouse['left_click_cur'] = 0
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            dragging_node = False
            dragging_node_index = -1
            if line_mode == True:
                line_mode = False
                create_edge()
                create_edge_new()

def open_tree():
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

def camera_pan():
    global is_panning_begin
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

def node_delete():
    global edges

    if node_focus_index >= 0:
        edges_keep = []
        for i in range(len(edges)):
            edge = edges[i]
            node_id = nodes[node_focus_index]['id']
            if edge['node_1_id'] != node_id and edge['node_2_id'] != node_id: 
                edges_keep.append(edge)
        edges = edges_keep
        del nodes[node_focus_index]

def init_edge_tmp():
    global line_mode
    for i, node in enumerate(nodes_new):
        x = get_socket_input_cx(node)
        y = get_socket_input_cy(node)
        if mouse['x'] >= x - 10 and mouse['y'] >= y - 10 and mouse['x'] <= x + 10 and mouse['y'] <= y + 10:
            line_tmp['x_1'] = x
            line_tmp['y_1'] = y
            line_mode = True
        x = get_socket_output_cx(node)
        y = get_socket_output_cy(node)
        if mouse['x'] >= x - 10 and mouse['y'] >= y - 10 and mouse['x'] <= x + 10 and mouse['y'] <= y + 10:
            line_tmp['x_1'] = x
            line_tmp['y_1'] = y
            line_mode = True

def draw_edge_tmp():
    if line_mode == True:
        x_1 = line_tmp['x_1']
        y_1 = line_tmp['y_1']
        x_2 = mouse['x']
        y_2 = mouse['y']
        pygame.draw.line(screen, '#ffffff', (x_1, y_1), (x_2, y_2))

def draw_edges_new():
    for edge in edges_new:
        socket_output_id = edge['socket_output']['id']
        x1 = -1
        y1 = -1
        x2 = -1
        y2 = -1
        for node in nodes_new:
            if node['socket_input'] != None:
                if node['socket_input']['id'] == edge['socket_input']['id']:
                    x1 = get_socket_input_cx(node)
                    y1 = get_socket_input_cy(node)
            if node['socket_output'] != None:
                if node['socket_output']['id'] == edge['socket_output']['id']:
                    x2 = get_socket_output_cx(node)
                    y2 = get_socket_output_cy(node)
        if x1 != -1 and y1 != -1 and x2 != -1 and y2 != -1:
            pygame.draw.line(screen, '#ffffff', (x1, y1), (x2, y2))

def create_edge():
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

def create_edge_new():
    for i, node in enumerate(nodes_new):
        x = get_socket_input_cx(node)
        y = get_socket_input_cy(node)
        if mouse['x'] >= x - 10 and mouse['y'] >= y - 10 and mouse['x'] <= x + 10 and mouse['y'] <= y + 10:
            # test data
            edge_new = {
                'id': 0,
                'socket_input': socket_0,
                'socket_output': socket_1,
            }
            edges_new.append(edge_new)

        x = get_socket_output_cx(node)
        y = get_socket_output_cy(node)
        if mouse['x'] >= x - 10 and mouse['y'] >= y - 10 and mouse['x'] <= x + 10 and mouse['y'] <= y + 10:
            # test data
            edge_new = {
                'id': 0,
                'socket_input': socket_0,
                'socket_output': socket_1,
            }
            edges_new.append(edge_new)
                            
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

def get_cell_hover():
    row_i = (mouse['y'] - camera['y']) // (64*camera['zoom'])
    col_i = (mouse['x'] - camera['x']) // (64*camera['zoom'])
    return row_i, col_i

def world_coords():
    x = mouse['x'] - camera['x']
    y = mouse['y'] - camera['y']
    return x, y

def mouse_main():
    # mouse_left()
    # mouse_right()
    pass

def mouse_right():
    if pygame.mouse.get_pressed()[2] == True:
        mouse['right_click_cur'] = 1
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            node_create()
    else:
        mouse['right_click_cur'] = 0
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            print('release')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('#101010')
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
            elif event.key == pygame.K_DELETE:
                node_delete()
            elif event.key == pygame.K_SPACE:
                node_create()
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

