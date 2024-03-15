import copy
from classes.gamestate import *
import time as t

def test_move_generation():   
    gamestates = [Gamestate()]
    while True:
        possible_game_states = []
        start_time = t.time()
        for gs in gamestates:
            possible_game_states.extend(gs.generate_all_moves(gs.is_white_to_move()))

        end_time = t.time()
        elapsed_time = end_time - start_time
        print(len(possible_game_states), 'possible move(s)')
        print('Execution time:', elapsed_time, 'seconds')

        gamestates = copy.deepcopy(possible_game_states)

test_move_generation()