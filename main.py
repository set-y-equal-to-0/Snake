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


# start is called when your Battlesnake begins a game
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


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")





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
    
    snake_list = list(snake for snake in game_state['board']['snakes'])

    for snake in snake_list:
        if snake['id'] == game_state['you']['id']:
            snake_list.remove(snake)
            break

    head_set = set()
    for snake in snake_list:

        head = snake['body'][0]
        head_set.add(P(head['x'], head['y']))

    my_head = P(game_state['you']['body'][0]['x'], game_state['you']['body'][0]['y']) 
    my_head_set = {my_head + J, my_head - J, my_head + I, my_head - I}

    potential_head_coords = set()
    for head in head_set:
        adjacent = head + J, head - J, head + I, head - I
        for point in adjacent:
            potential_head_coords.add(point)

    return my_head_set - potential_head_coords


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


def path_find(game_state):       
    
    adj = lambda point: {point + J, point - J, point + I, point - I}
    any_adj = lambda ntwk_set, adj_set: reduce(lambda a, b: a or b, (neighbour in ntwk_set for neighbour in adj_set), 0)

    occupied_set = get_occupied(game_state)
    clear_set = BOARD_SET - occupied_set
    my_head = P(game_state['you']['body'][0]['x'], game_state['you']['body'][0]['y'])
    group_dict = {}

    valid_adj = adj(my_head) - occupied_set
    for square in valid_adj:
        network_set = set()
        try:   
            clear_set.remove(square)
            network_set.add(square)
            while True:
                length = len(network_set)
                for space in clear_set:
                    if any_adj(network_set, adj(space) - occupied_set):
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

    return list((V_TO_D[point - my_head], len(set)) for point, set in group_dict.items())


def move(game_state: typing.Dict) -> typing.Dict:

    valid_moves_set = {'left', 'right', 'up', 'down'}

    my_head = P(game_state["you"]["body"][0]['x'], game_state["you"]["body"][0]['y'])  # Coordinates of my head

    food_list = list(P(coord_dict['x'], coord_dict['y']) for coord_dict in game_state['board']['food'])
    food_list.sort(key = lambda food: len(food - my_head))

    occupied_set = get_occupied(game_state)

    if my_head + I in occupied_set or my_head.x == WIDTH - 1:
        valid_moves_set.remove('right')

    if my_head - I in occupied_set or my_head.x == 0:
        valid_moves_set.remove('left')

    if my_head + J in occupied_set or my_head.y == HEIGHT - 1:
        valid_moves_set.remove('up')

    if my_head - J in occupied_set or my_head.y == 0:
        valid_moves_set.remove('down')

    food_direction_set = set()

    for food in food_list:

        food_direction_set = get_directions(food - my_head)
        food_direction_set &= valid_moves_set
        
        if len(food_direction_set) > 0:
            break

    center_direction_set = get_directions(CENTER - my_head)
    center_direction_set &= valid_moves_set

    no_heads_set = get_head_potiential(game_state)
    avoid_head_directions = set()

    for pos in no_heads_set:
        avoid_head_directions |= get_directions(pos - my_head)

    avoid_head_directions &= valid_moves_set

    group_list = path_find(game_state)
    group_list.sort(key = lambda e: e[1], reverse = True)
    group_set = {e[0] for e in group_list if e[1] == group_list[0][1]}

    if not valid_moves_set:
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
        next_move = valid_moves_set.pop()

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
