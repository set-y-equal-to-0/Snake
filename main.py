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
import numpy as np



ADD = lambda coord, offset: (coord[0] + offset[0], coord[1] + offset[1])
SUB = lambda coord, offset: (coord[0] - offset[0], coord[1] - offset[1])



I, J = (1, 0), (0, 1)





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

    global WIDTH
    global HEIGHT
    global BOARD_SET
    WIDTH, HEIGHT = game_state['board']['width'], game_state['board']['height']
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
    print(BOARD_SET)
    return empty_spaces


    

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

    if my_head[0] == WIDTH - 1 or ADD(my_head, I) not in empty_spaces_set:
        moves_set.remove('right')

    if my_head[0] == 0 or SUB(my_head, I) not in empty_spaces_set:
        moves_set.remove('left')

    if my_head[1] == HEIGHT - 1 or ADD(my_head, J) not in empty_spaces_set:
        moves_set.remove('up')

    if my_head[1] == 0 or SUB(my_head, J) not in empty_spaces_set:
        moves_set.remove('down')

    food_direction = set()

    for food in food_list:

        diff = SUB(food, my_head)

        if diff[0] > 0:
            food_direction.add('right')

        if diff[0] < 0:
            food_direction.add('left')

        if diff[1] > 0:
            food_direction.add('up')

        if diff[1] < 0:
            food_direction.add('down')

        food_direction &= moves_set
        
        if len(food_direction) > 0:

            next_move = food_direction.pop()
            break

    if len(moves_set) > 0 and next_move is None:
        next_move = moves_set.pop()

    if next_move is None:
        next_move = 'down'


    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
