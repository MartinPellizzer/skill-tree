import pygame

pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])

is_panning_begin = False

# TODO: filepath to json skill tree

nodes = []
edges = []

nodes.append({
    'id': 2,
    'x': 100,
    'y': 300,
    'w': 160,
    'h': 36,
    'text': 'Plants Benefits Art',
})

nodes.append({
    'id': 3,
    'x': 300,
    'y': 300,
    'w': 160,
    'h': 36,
    'text': 'Studies - LV 0/5',
})

nodes.append({
    'id': 0,
    'x': 100,
    'y': 100,
    'w': 160,
    'h': 36,
    'text': 'skill tree - LV 1/5',
})

nodes.append({
    'id': 1,
    'x': 400,
    'y': 100,
    'w': 160,
    'h': 36,
    'text': 'pad - LV 1/5',
})

edges.append({
    'id': 0,
    'node_1_id': 0,
    'node_2_id': 1,
})

edges.append({
    'id': 1,
    'node_1_id': 2,
    'node_2_id': 3,
})

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

    screen.fill('#101010')

    # inputs/update
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()

    # drag
    if dragging_node == True:
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

    # drag
    if pygame.mouse.get_pressed()[0] == True: # left click
        mouse['left_click_cur'] = 1
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            for i, node in enumerate(nodes):
                x_1 = (node['x'] + camera['x']) * camera['zoom']
                y_1 = (node['y'] + camera['y']) * camera['zoom']
                x_2 = (node['x'] + node['w'] + camera['x']) * camera['zoom']
                y_2 = (node['y'] + node['h'] + camera['y']) * camera['zoom']
                if mouse['x'] >= x_1 and mouse['y'] >= y_1 and mouse['x'] < x_2 and mouse['y'] < y_2:
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
        
    # add node
    if pygame.mouse.get_pressed()[2] == True: # right click
        mouse['right_click_cur'] = 1
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            nodes.append({
                'id': 0,
                'x': mouse['x'],
                'y': mouse['y'],
                'w': 100,
                'h': 100,
            })
            print('click')
    else:
        mouse['right_click_cur'] = 0
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            print('release')
        
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

    # draw
    for node in nodes:
        x = (node['x'] + camera['x']) * camera['zoom']
        y = (node['y'] + camera['y']) * camera['zoom']
        w = (node['w']) * camera['zoom']
        h = (node['h']) * camera['zoom']
        pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), )
        pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)
        px = 8
        py = 8
        font = pygame.font.SysFont('Arial', 16)
        text_surface = font.render(f'{node["text"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x + px, y + py))



    # debug
    y = 24

    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(f'x: {mouse["x"]} - y: {mouse["y"]}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24

    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(f'camera_x: {camera["x"]} - camera_y: {camera["y"]}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24

    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(f'camera_zoom: {camera["zoom"]}', False, (255, 255, 255))
    screen.blit(text_surface, (0, y))
    y += 24

    pygame.display.flip()

pygame.quit()
