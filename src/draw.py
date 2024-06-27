from classes.button import *
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images() -> None:
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 
              'p', 'r', 'n', 'b', 'q', 'k']
    for piece in pieces:
        if piece.isupper():
            piece = 'w' + piece
        IMAGES[piece] = p.image.load("./img/" + piece + ".png")

def draw_gamestate(screen, board: List[int], player_is_white) -> None:
    draw_board(screen)
    draw_pieces(screen, board, player_is_white)

def draw_board(screen) -> None:
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, player_is_white) -> None:
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            
            if piece != "-":
                if piece.isupper():
                    piece = 'w' + piece
                if player_is_white:
                    screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    screen.blit(IMAGES[piece], p.Rect((7-c)*SQ_SIZE, (7-r)*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def update_board(screen, clock, matrix, player_is_white) -> None:
    draw_gamestate(screen, matrix, player_is_white)
    clock.tick(MAX_FPS)
    p.display.flip()
 
def run_menu() -> None:

    button1 = Button(5, 100, 500, 75, (235, 64, 52), 'PLAY A FRIEND')
    button2 = Button(5, 312, 500, 75, (235, 64, 52), 'PLAY THE LOTUS CHESS ENGINE')
    button3 = Button(5, 100, 500, 75, (235, 64, 52), 'PLAY AS WHITE')
    button4 = Button(5, 312, 500, 75, (235, 64, 52), 'PLAY AS BLACK')

    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONUP:
                if event.button == 1: 
                    if button1.rect.collidepoint(event.pos):
                        return False, True
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



