import copy
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

def player_moves(gs, possible_game_states):
    if gs.white_to_move_flag:
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

    new_gs = copy.deepcopy(gs)

    if (piece == 'K' and end_col == col + 2 and end_row == row) or (piece == 'k' and end_col == col + 2 and end_row == row):
        new_gs.board[row][col] = '-'
        new_gs.board[end_row][end_col] = piece
        new_gs.board[row][col+3] = '-'
        new_gs.board[end_row][end_col-1] = 'R'

    else:
        new_gs.board[row][col] = '-'
        new_gs.board[end_row][end_col] = piece

        if (piece == 'P' and end_row == row - 2):
            new_gs.ep_flag_array[0][col] = True
        elif (piece == 'p' and end_row == row + 2):
            new_gs.ep_flag_array[1][col] = True

    possible_game_boards = []
    for ele in possible_game_states:
        possible_game_boards.append(ele.board)
    if new_gs.board in possible_game_boards:
        new_gs.white_to_move_flag = not new_gs.white_to_move_flag
        return new_gs
    else:
        return player_moves(gs, possible_game_states)
    