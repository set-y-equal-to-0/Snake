# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import typing
from functools import reduce








# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "set-y-equal-to-0",  # TODO: Your Battlesnake Username
        "color": "#3ade94",  # TODO: Choose color
        "head": "do-sammy",  # TODO: Choose head
        "tail": "do-sammy",  # TODO: Choose tail
    }

def start(game_state: typing.Dict):
    print("GAME START")

    global I
    global J
    I = (1, 0)
    J = (0, 1)

    global WIDTH
    global HEIGHT
    WIDTH, HEIGHT = game_state['board']['width'], game_state['board']['height']

    global CENTER
    CENTER = (WIDTH // 2, HEIGHT // 2)

    global BOARD_SET
    BOARD_SET = {(x, y) for x in range(WIDTH) for y in range(HEIGHT)}

    global D_TO_V
    global V_TO_D
    D_TO_V = {'left': (-1, 0), 'right': I, 'up': J, 'down': (0, -1)}
    V_TO_D = {(-1, 0): 'left', I: 'right', J: 'up', (0, -1): 'down'}

    global DIST
    DIST = lambda tup1, tup2: abs(tup1[0] - tup2[0]) + abs(tup1[1] - tup2[1])

    global ADD
    ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

    global SUB
    SUB = lambda a, b: (a[0] - b[0], a[1] - b[1])

def end(game_state: typing.Dict):
    print("GAME OVER\n")



def first(game_state):

    info = {}

    # get occupied squares
    snake_list = game_state['board']['snakes']
    hazards_list = game_state['board']['hazards']
    OCCUPIED = set()

    for snake in snake_list:
        for coord_dict in snake['body']:
            OCCUPIED.add((coord_dict['x'], coord_dict['y']))

    for hazard_dict in hazards_list:
        OCCUPIED.add((hazard_dict['x'], hazard_dict['y']))

    info['occupied'] = OCCUPIED
 
    info['clear'] = BOARD_SET - OCCUPIED

    info['my_head'] = game_state['you']['body'][0]['x'], game_state['you']['body'][0]['y']

    info['head_adj'] = get_valid_adj(info, info['my_head'], direction=False)

    food_list = list((coord_dict['x'], coord_dict['y']) for coord_dict in game_state['board']['food'])
    food_list.sort(key = lambda food: DIST(food, info['my_head']))
    info['food'] = food_list

    info['valid_moves'] = get_valid_adj(info, info['my_head'])

    info['potential_heads'] = get_head_potiential(game_state)
 
    info['areas'] = new_path(info, info['my_head'], info['head_adj'])

    return info


def get_valid_adj(info, point, direction = True):

    if direction:
        valid_moves_set = {'left', 'right', 'up', 'down'}
        direction_dict = {'r': 'right', 'l': 'left', 'u': 'up', 'd': 'down'}

    else:
        valid_moves_set = {ADD(point, I), SUB(point, I), ADD(point, J),  SUB(point, J)}
        direction_dict = {'r': ADD(point, I), 'l': SUB(point, I), 'u': ADD(point, J), 'd': SUB(point, J)}

    if ADD(point, I) in info['occupied'] or point[0] == WIDTH - 1:
        valid_moves_set.remove(direction_dict['r'])

    if SUB(point, I) in info['occupied'] or point[0] == 0:
        valid_moves_set.remove(direction_dict['l'])

    if ADD(point, J) in info['occupied'] or point[1] == HEIGHT - 1:
        valid_moves_set.remove(direction_dict['u'])

    if SUB(point, J) in info['occupied'] or point[1] == 0:
        valid_moves_set.remove(direction_dict['d'])

    return valid_moves_set


def get_head_potiential(game_state):
    
    snake_list = game_state['board']['snakes']
    head_set = set()
    potential_head_coords = set()

    for snake in snake_list:
        if snake['id'] != game_state['you']['id']:
            head = snake['body'][0]
            head_set.add((head['x'], head['y']))
    
    for head in head_set:
        adjacent = ADD(head, I), SUB(head, I), ADD(head, J), SUB(head, J)
        for point in adjacent:
            potential_head_coords.add(point)

    return potential_head_coords


def get_directions(vector: typing.Tuple[int,int]):

    direction_set = set()

    if vector[0] > 0:
       direction_set.add('right')

    if vector[0] < 0:
        direction_set.add('left')

    if vector[1] > 0:
        direction_set.add('up')

    if vector[1] < 0:
        direction_set.add('down')

    return direction_set


#def path_find():       
    
    any_adj = lambda ntwk_set, adj_set: reduce(lambda a, b: a or b, (neighbour in ntwk_set for neighbour in adj_set), 0)
    clear_set = BOARD_SET - occupied_set
    
    group_dict = {}

    valid_adj = my_head_adj - occupied_set
    for square in valid_adj:
        network_set = set()
        try:   
            clear_set.remove(square)
            network_set.add(square)
            while True:
                length = len(network_set)
                for space in clear_set:
                    if any_adj(network_set, GET_ADJ(space) - occupied_set):
                        network_set.add(space)      
                if length == len(network_set):
                    break
                
            clear_set -= network_set
            group_dict[square] = network_set

        except KeyError:
            continue

    temp_dict = {}
    for point in valid_adj - set(group_dict.keys()):
        for value in group_dict.values():
            if point in value:
                temp_dict[point] = value
    group_dict |= temp_dict

    summary_list = list((V_TO_D[point - my_head], len(set)) for point, set in group_dict.items())
    return summary_list.sort(key = lambda e: e[1], reverse = True)


def new_path(info, my_head, my_head_adj, network_set = set(), group_dict = {}, adj_set = None, index = 0):

    if index == 0:
        adj_set = my_head_adj
        group_dict.clear()
        network_set.clear()
        total_set = set()

    for point in adj_set:
        if (index > 0 and point not in network_set) or (index == 0 and point not in total_set):
            network_set.add(point)
            network_set = new_path(info, my_head, my_head_adj, network_set, None, get_valid_adj(info, point, direction = False), index + 1)
            if index == 0: 
                group_dict[point] = frozenset(network_set)
                total_set |= network_set
                network_set.clear()

    if index > 0:
        return network_set

    temp_dict = {}
    for point in my_head_adj - set(group_dict.keys()):
        for value in group_dict.values():
            if point in value:
                temp_dict[point] = value
    group_dict |= temp_dict

    summary_list = list((V_TO_D[SUB(point, my_head)], len(set), set) for point, set in group_dict.items())
    summary_list.sort(key = lambda e: e[1], reverse = True)
    return summary_list


def move(game_state: typing.Dict) -> typing.Dict:

    info = first(game_state)

    food_direction_set = set()
    for food in info['food']:
        food_direction_set = get_directions(SUB(food, info['my_head']))
        food_direction_set &= info['valid_moves']  
        if len(food_direction_set) > 0:
            break

    center_direction_set = get_directions(SUB(CENTER, info['my_head']))
    center_direction_set &= info['valid_moves']

    no_heads_set = info['head_adj'] - get_head_potiential(game_state)
    avoid_head_directions = set()
    for pos in no_heads_set:
        avoid_head_directions |= get_directions(SUB(pos, info['my_head']))
    avoid_head_directions &= info['valid_moves']

    group_set = {e[0] for e in info['areas'] if e[1] == info['areas'][0][1]}

    if not info['valid_moves']:
        next_move = 'down'

    elif avoid_head_directions & group_set & food_direction_set:
        next_move = (avoid_head_directions & group_set & food_direction_set).pop()

    elif avoid_head_directions & group_set:
        next_move = (avoid_head_directions & group_set).pop()

    elif avoid_head_directions & food_direction_set:
        next_move = (avoid_head_directions & food_direction_set).pop()

    elif avoid_head_directions & center_direction_set:
        next_move = (avoid_head_directions & center_direction_set).pop()

    elif avoid_head_directions:
        next_move = avoid_head_directions.pop()

    else:
        next_move = info['valid_moves'].pop()

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
