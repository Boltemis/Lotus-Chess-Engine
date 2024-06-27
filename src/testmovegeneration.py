from classes.gamestate import *
from utils import *
import time as t

START_FLAGS: dict[str: bool] = {
    "white_king_moved": False, 
    "left_white_rook_moved": False, 
    "right_white_rook_moved": False, 
    "black_king_moved": False,
    "left_black_rook_moved": False, 
    "right_black_rook_moved": False, 
    "white_to_move": True
    }

START_BOARD: List[str] = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

def test_move_generation():   
    gamestates = [Gamestate(Board(START_BOARD), START_FLAGS, 0, 32, 0)]
    while True:
        print("\nNext Iteration: ")
        checkmate_counter = 0
        new_gamestates = []
        start_time = t.time()
        for gs in gamestates:
            if len(gs.possible_moves) == 0:
                new_gamestates.extend(gs.generate_all_moves())
            if gs.is_checkmate():
                checkmate_counter += 1
        end_time = t.time()
        elapsed_time = end_time - start_time

        print('Execution time generating moves:', elapsed_time, 'seconds')
        print(len(new_gamestates), 'possible move(s)')
        print('Amount of checkmates found:', checkmate_counter)
        
        gamestates = new_gamestates

test_move_generation()