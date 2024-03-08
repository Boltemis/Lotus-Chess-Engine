from draw import *
import time as t

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
    current_gs = Gamestate()
    possible_game_states = [current_gs]
    update_board(screen, clock, current_gs)

    # game loop
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
   
        start_time = t.time()       
        possible_game_states = generate_all_moves(current_gs, current_gs.is_white_to_move)
        
        end_time = t.time()
        elapsed_time = end_time - start_time

        if versus_engine:
            if (player_is_white and current_gs.is_white_to_move) or (not player_is_white and not current_gs.is_white_to_move):

                current_gs = player_moves(current_gs, possible_game_states)
            else:
                if player_is_white:
                    current_gs = minimax(current_gs, 2, -999999, 999999, "white")[1]
                else:
                    current_gs = minimax(current_gs, 2, -999999, 999999, "black")[1]
        else:
            current_gs = player_moves(current_gs, possible_game_states)

        update_board(screen, clock, current_gs)

        print(len(possible_game_states), 'possible move(s)')
        print('Execution time:', elapsed_time, 'seconds')

        if current_gs.is_checkmate():
            print("GAME OVER, CHECKMATE")
            running = False
        elif current_gs.is_stalemate():
            print("GAME OVER, STALEMATE")
            running = False

if __name__ == "__main__":
    main()