from time import sleep
from typing import List
import pygame as p

def board_to_fen(board) -> str:
    """ converts a board state to FEN """
    fen = ''
    for row in board:
        counter = 0
        for square in row:
            if square == '-':
                counter += 1
            else:
                if counter:
                    fen += str(counter)
                    counter = 0
                fen += square   
        if counter:
            fen += str(counter)
        fen += '/'
    return fen[:-1]

def fen_to_board(fen) -> List[List[str]]:
    """ converts a FEN to a board state """
    board = [[] for _ in range(8)]
    row = 0
    for char in fen:
        if char.isdigit() and 1 <= int(char) <= 8:
            for _ in range(int(char)):
                board[row].append('-')
        elif char == '/':
            row += 1
        else:
            board[row].append(char)
    return board    

def print_board(board):
    for i in range(8):
        print(board[i])
    print()
    return


def display_moves(moves):
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

    def draw_gamestate(screen, gs) -> None:
        draw_board(screen)
        draw_pieces(screen, gs)

    def draw_board(screen) -> None:
        colors = [p.Color("white"), p.Color("gray")]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[((r+c) % 2)]
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def draw_pieces(screen, board) -> None:
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                
                if piece != "-":
                    if piece.isupper():
                        piece = 'w' + piece
                    screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def update_board(screen, clock, gs) -> None:
        draw_gamestate(screen, gs.board)
        clock.tick(MAX_FPS)
        p.display.flip()

    set_up_pygame()
    # set up game
    load_images()
    for move in moves:
        update_board(screen, clock, move)
        sleep(5)

    