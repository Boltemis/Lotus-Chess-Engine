from classes.gamestate import Gamestate
from classes.move import Move

import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

def player_moves(gs, possible_moves) -> Gamestate: 
    wait = p.event.wait()
    while wait.type != p.MOUSEBUTTONDOWN:
        wait = p.event.wait()
    
    pos = p.mouse.get_pos()
    col = pos[0] // SQ_SIZE
    row = pos[1] // SQ_SIZE
    
    wait = p.event.wait()
    while wait.type != p.MOUSEBUTTONDOWN:
        wait = p.event.wait()

    pos = p.mouse.get_pos()
    end_col = pos[0] // SQ_SIZE
    end_row = pos[1] // SQ_SIZE

    new_move = Move(row, col, end_row, end_col)
    for move in possible_moves:
        if new_move.equals(move):
            return gs.apply_move(new_move)
    print("Invalid move..")
    return player_moves(gs, possible_moves)
    