from classes.gamestate import *
from move_generation import *
import time as t
import cProfile

def testfunc() -> None:
    startgs = Gamestate()

    all_states = [startgs]
    start_time = t.time()  

    while len(all_states) < 9000:
        new_states = []
        for ele in all_states:
            if ele.white_to_move_flag:
                new_states.extend(all_white_moves(ele, False))
            else:
                new_states.extend(all_black_moves(ele, False))

        end_time = t.time()
        elapsed_time = end_time-start_time

        print(len(all_states), 'possible move(s)')
        print('Execution time:', elapsed_time, 'seconds')

        all_states = new_states

    return
cProfile.run('testfunc()')