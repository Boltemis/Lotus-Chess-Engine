from evaluation import *
from classes import *
from move import *
from playermode import *
import pygame as p
import time as t
import random as r

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 
              'p', 'r', 'n', 'b', 'q', 'k']
    for piece in pieces:
        if piece.isupper():
            piece = 'w' + piece
        IMAGES[piece] = p.image.load("./img/" + piece + ".png")

def draw_gamestate(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            
            if piece != "-":
                if piece.isupper():
                    piece = 'w' + piece
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def update_board(screen, clock, gs):
    draw_gamestate(screen, gs.board)
    clock.tick(MAX_FPS)
    p.display.flip()
 
def run_menu():

    button1 = Button(5, 100, 500, 75, (235, 64, 52), 'PLAY A FRIEND')
    button2 = Button(5, 312, 500, 75, (235, 64, 52), 'PLAY THE LOTUS CHESS ENGINE')
    button3 = Button(5, 100, 500, 75, (235, 64, 52), 'PLAY AS WHITE')
    button4 = Button(5, 312, 500, 75, (235, 64, 52), 'PLAY AS BLACK')

    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONUP:
                if event.button == 1: 
                    if button1.rect.collidepoint(event.pos):
                        return False, False
                    elif button2.rect.collidepoint(event.pos):
                        while True:
                            for event in p.event.get():
                                if event.type == p.MOUSEBUTTONUP:
                                    if event.button == 1: 
                                        if button3.rect.collidepoint(event.pos):
                                            return True, True
                                        elif button4.rect.collidepoint(event.pos):
                                            return True, False
                            
                            button3.draw()
                            button4.draw()
                            p.display.flip()
             
        button1.draw()
        button2.draw()
        p.display.flip()

def set_up_pygame():
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

        new_states = []    
        start_time = t.time()  
        if current_gs.white_to_move_flag:
            new_states = all_white_moves(current_gs)
        else:
            new_states = all_black_moves(current_gs)

        
        possible_game_states = new_states

        if versus_engine:
            if (player_is_white and current_gs.white_to_move_flag) or (not player_is_white and not current_gs.white_to_move_flag):

                current_gs = player_moves(current_gs, possible_game_states)
            else:
                if player_is_white:
                    current_gs = minimax(current_gs, 2, -999999, 999999, "white")[1]
                else:
                    current_gs = minimax(current_gs, 2, -999999, 999999, "black")[1]
        else:
            current_gs = player_moves(current_gs, possible_game_states)

        update_board(screen, clock, current_gs)

        end_time = t.time()
        elapsed_time = end_time - start_time

        print(len(possible_game_states), 'possible move(s)')
        print('Execution time:', elapsed_time, 'seconds')

        if is_checkmate(current_gs):
            print("GAME OVER, CHECKMATE")
            running = False
        elif is_stalemate(current_gs):
            print("GAME OVER, STALEMATE")
            running = False

if __name__ == "__main__":
    main()