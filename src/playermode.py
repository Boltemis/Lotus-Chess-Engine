from classes.gamestate import Gamestate
from classes.move import Move

import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

def player_moves(gs, possible_moves, player_is_white) -> Gamestate: 
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

    if player_is_white:
        new_move = gs.apply_move(Move(row, col, end_row, end_col))
    else:
        new_move = gs.apply_move(Move(7-row, 7-col, 7-end_row, 7-end_col))
    for move in possible_moves:
        if new_move == move:
            return new_move
    print("Invalid move..")
    return player_moves(gs, possible_moves, player_is_white)
    