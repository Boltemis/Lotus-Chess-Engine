import pygame as p

from classes.gamestate import Gamestate

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

def player_moves(gs, possible_game_states) -> Gamestate: 
    if gs.is_white_to_move():
        print("White to move")
    else:
        print("Black to move")

    wait = p.event.wait()
    while wait.type != p.MOUSEBUTTONDOWN:
        wait = p.event.wait()
    
    pos = p.mouse.get_pos()
    col = pos[0] // SQ_SIZE
    row = pos[1] // SQ_SIZE
    piece = gs.board[row][col]
    
    wait = p.event.wait()
    while wait.type != p.MOUSEBUTTONDOWN:
        wait = p.event.wait()

    pos = p.mouse.get_pos()
    end_col = pos[0] // SQ_SIZE
    end_row = pos[1] // SQ_SIZE

    new_move = [ele[:] for ele in gs.board]

    new_move[row][col] = '-'
    new_move[end_row][end_col] = piece

    new_gs = gs.copy(new_move)
    new_gs.change_player()
    possible_game_boards = []
    for ele in possible_game_states:
        possible_game_boards.append(ele.board) 

    if new_gs.board in possible_game_boards:
        return new_gs
    else:
        return player_moves(gs, possible_game_states)
    