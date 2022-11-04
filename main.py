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

    global ADD
    global SUB
    ADD = lambda coord, offset: (coord[0] + offset[0], coord[1] + offset[1])
    SUB = lambda coord, offset: (coord[0] - offset[0], coord[1] - offset[1])
    
    global I
    global J
    I, J = (1, 0), (0, 1)

    global WIDTH
    global HEIGHT
    WIDTH, HEIGHT = game_state['board']['width'], game_state['board']['height']

    global CENTER
    CENTER = WIDTH // 2, HEIGHT // 2

    global BOARD_SET
    BOARD_SET = set((x, y) for x in range(0, WIDTH) for y in range(0, HEIGHT))
    

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")





def get_empty_spaces(game_state) -> typing.Set:

    snake_list = game_state['board']['snakes']
    occupied = set()

    for snake in snake_list:
        for coord_dict in snake['body']:
            coord = (coord_dict['x'], coord_dict['y'])
            occupied.add(coord)

    empty_spaces = BOARD_SET - occupied
    return empty_spaces
 

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



# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    moves_set = {'left', 'right', 'up', 'down'}

    my_head = game_state["you"]["body"][0]['x'], game_state["you"]["body"][0]['y']  # Coordinates of my head

    next_move = None

    food_list = list((coord_dict['x'], coord_dict['y']) for coord_dict in game_state['board']['food'])
    food_list.sort(key = lambda food: abs(my_head[0] - food[0]) + abs(my_head[1] - food[1]))

    empty_spaces_set = get_empty_spaces(game_state)

    if ADD(my_head, I) not in empty_spaces_set:
        moves_set.remove('right')

    if SUB(my_head, I) not in empty_spaces_set:
        moves_set.remove('left')

    if ADD(my_head, J) not in empty_spaces_set:
        moves_set.remove('up')

    if SUB(my_head, J) not in empty_spaces_set:
        moves_set.remove('down')

    for food in food_list:

        diff = SUB(food, my_head)

        food_direction_set = get_directions(diff)

        food_direction_set &= moves_set
        
        if len(food_direction_set) > 0:
            break

    center_direction_set = get_directions(SUB(CENTER, my_head))
    center_direction_set &= moves_set

    if len(moves_set) == 0:
        next_move = 'down'

    elif len(food_direction_set) > 0:
        next_move = food_direction_set.pop()

    elif len(center_direction_set) > 0 and game_state['you']['health'] < 60:
        next_move = center_direction_set.pop()

    else:
        next_move = moves_set.pop()


    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
