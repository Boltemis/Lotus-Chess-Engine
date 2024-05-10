from draw import *
from playermode import *
from evaluation import *
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

screen = p.display.set_mode((800, 600))

def set_up_pygame() -> None:
    global clock
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Lotus Chess Engine')
    icon = p.image.load('./img/icon.png')
    p.display.set_icon(icon)
    clock = p.time.Clock()
    screen.fill(p.Color(79, 240, 192))

def main():
    # set up menu
    set_up_pygame()
    versus_engine, player_is_white = run_menu()

    # set up game
    load_images()
    current_gs = Gamestate(Board(START_BOARD), START_FLAGS, 0, 32, 0)
    update_board(screen, clock, current_gs)

    # game loop
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
   
        start_time = t.time()       
        current_gs.generate_all_moves()

        if versus_engine:
            if (player_is_white == current_gs.is_white_to_move()):
                current_gs = player_moves(current_gs, current_gs.possible_moves)
            else:
                current_gs = minimax(current_gs, 3, -999999, 999999, current_gs.is_white_to_move())[1]

        else:
            current_gs = player_moves(current_gs, current_gs.possible_moves)

        end_time = t.time()
        elapsed_time = end_time - start_time
        
        update_board(screen, clock, current_gs)

        print(len(current_gs.possible_moves), 'possible move(s)')
        print('Execution time:', elapsed_time, 'seconds')

        if current_gs.is_checkmate():
            print("GAME OVER, CHECKMATE")
            running = False
        elif current_gs.is_stalemate():
            print("GAME OVER, STALEMATE")
            running = False

if __name__ == "__main__":
    main()