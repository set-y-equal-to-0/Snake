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

import random
import typing
from point_class import V2 as P
from functools import reduce
import time







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
    I = P(1, 0)
    J = P(0, 1)

    global WIDTH
    global HEIGHT
    WIDTH, HEIGHT = game_state['board']['width'], game_state['board']['height']

    global CENTER
    CENTER = P(WIDTH // 2, HEIGHT // 2)

    global BOARD_SET
    BOARD_SET = {P(x, y) for x in range(WIDTH) for y in range(HEIGHT)}

    global D_TO_V
    global V_TO_D
    D_TO_V = {'left': P(-1, 0), 'right': I, 'up': J, 'down': P(0, -1)}
    V_TO_D = {P(-1, 0): 'left', I: 'right', J: 'up', P(0, -1): 'down'}

    global MOVE_PRIORITY

def end(game_state: typing.Dict):
    print("GAME OVER\n")



def first(game_state):

    occupied_set = get_occupied(game_state)
 
    clear_set = BOARD_SET - occupied_set

    my_head = P(game_state['you']['body'][0]['x'], game_state['you']['body'][0]['y'])

    my_head_adj = get_valid_adj(occupied_set, my_head, direction = False)

    food_list = list(P(coord_dict['x'], coord_dict['y']) for coord_dict in game_state['board']['food'])
    food_list.sort(key = lambda food: len(food - my_head))

    valid_moves_set = get_valid_adj(occupied_set, my_head)

    potential_heads = get_head_potiential(game_state)
 
    area_list = new_path(occupied_set, my_head, my_head_adj)

    print({'occupied': occupied_set, 'clear': clear_set, 'my_head': my_head, 'my_head_adj': my_head_adj, 'food_list': food_list, 'valid_moves_set': valid_moves_set, 'potential_heads': potential_heads, 'area_list': area_list})

    return {'occupied': occupied_set, 'clear': clear_set, 'my_head': my_head, 'my_head_adj': my_head_adj, 
            'food_list': food_list, 'valid_moves_set': valid_moves_set, 'potential_heads': potential_heads, 'area_list': area_list}


def get_valid_adj(occupied_set, point, direction = True):

    if direction:
        valid_moves_set = {'left', 'right', 'up', 'down'}
        direction_dict = {'r': 'right', 'l': 'left', 'u': 'up', 'd': 'down'}

    else:
        valid_moves_set = {point + I, point - I, point + J,  point - J}
        direction_dict = {'r': point + I, 'l': point - I, 'u': point + J, 'd': point - J}

    if point + I in occupied_set or point.x == WIDTH - 1:
        valid_moves_set.remove(direction_dict['r'])

    if point - I in occupied_set or point.x == 0:
        valid_moves_set.remove(direction_dict['l'])

    if point + J in occupied_set or point.y == HEIGHT - 1:
        valid_moves_set.remove(direction_dict['u'])

    if point - J in occupied_set or point.y == 0:
        valid_moves_set.remove(direction_dict['d'])

    return valid_moves_set


def get_occupied(game_state) -> typing.Set:

    snake_list = game_state['board']['snakes']

    hazards_list = game_state['board']['hazards']
    occupied = set()

    for snake in snake_list:
        for coord_dict in snake['body']:
            occupied.add(P(coord_dict['x'], coord_dict['y']))

    for hazard_dict in hazards_list:
        coord = P(hazard_dict['x'], hazard_dict['y'])
        occupied.add(coord)

    return occupied
 

def get_head_potiential(game_state):
    
    snake_list = game_state['board']['snakes']
    head_set = set()
    potential_head_coords = set()

    for snake in snake_list:
        if snake['id'] != game_state['you']['id']:
            head = snake['body'][0]
            head_set.add(P(head['x'], head['y']))
    
    for head in head_set:
        adjacent = head + J, head - J, head + I, head - I
        for point in adjacent:
            potential_head_coords.add(point)

    return potential_head_coords


def get_directions(vector: typing.Tuple[int,int]):

    direction_set = set()

    if vector.x > 0:
       direction_set.add('right')

    if vector.x < 0:
        direction_set.add('left')

    if vector.y > 0:
        direction_set.add('up')

    if vector.y < 0:
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


def new_path(occupied, my_head, my_head_adj, network_set = set(), group_dict = {}, adj_set = None, index = 0):

    if index == 0:
        adj_set = my_head_adj
        group_dict.clear()
        network_set.clear()
        total_set = set()

    for point in adj_set:
        if (index > 0 and point not in network_set) or (index == 0 and point not in total_set):
            network_set.add(point)
            network_set = new_path(occupied, my_head, my_head_adj, network_set, None, get_valid_adj(occupied, point, direction = False), index + 1)
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

    summary_list = list((V_TO_D[point - my_head], len(set), set) for point, set in group_dict.items())
    summary_list.sort(key = lambda e: e[1], reverse = True)
    return summary_list


def move(game_state: typing.Dict) -> typing.Dict:

    d = first(game_state)

    food_direction_set = set()
    for food in d['food_list']:
        food_direction_set = get_directions(food - d['my_head'])
        food_direction_set &= d['valid_moves_set']  
        if len(food_direction_set) > 0:
            break

    center_direction_set = get_directions(CENTER - d['my_head'])
    center_direction_set &= d['valid_moves_set']

    no_heads_set = d['my_head_adj'] - get_head_potiential(game_state)
    avoid_head_directions = set()
    for pos in no_heads_set:
        avoid_head_directions |= get_directions(pos - d['my_head'])
    avoid_head_directions &= d['valid_moves_set']

    group_set = {e[0] for e in d['area_list'] if e[1] == d['area_list'][0][1]}

    for direc, size, group in d['area_list']:
        if d['food_list'][-1] in group and game_state['you']['health'] > 30:
            return {"move": next_move}

    if not d['valid_moves_set']:
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
        next_move = d['valid_moves_set'].pop()

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
