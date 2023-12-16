from classes import *
from playermode import *
import copy

def is_white_in_check(gs):
    moves = all_black_moves(gs, False)
    for ele in moves:
        if not any('K' in row for row in ele.board):
            return True
    return False

def is_black_in_check(gs):
    moves = all_white_moves(gs, False)
    for ele in moves:
        if not any('k' in row for row in ele.board):
            return True
    return False

def is_checkmate(gs):
    if is_white_in_check(gs):
        moves = all_white_moves(gs)
        for move in moves:
            if not is_white_in_check(move):
                return False
        return True
    elif is_black_in_check(gs):
        moves = all_black_moves(gs)
        for move in moves:
            if not is_black_in_check(move):
                return False
        return True
    return False

def is_stalemate(gs):
    if gs.white_to_move_flag:
        if len(all_white_moves(gs)) == 0 and not is_white_in_check(gs):
            return True
    else:
        if len(all_black_moves(gs)) == 0 and not is_black_in_check(gs):
            return True
    
    return False

def make_move(gs, start_row, start_col, end_row, end_col, piece):
    new_gs = copy.deepcopy(gs)
    new_gs.board[start_row][start_col] = '-'
    new_gs.board[end_row][end_col] = piece
    new_gs.ep_flag_array = [[False] * 8 for _ in range(2)]
    if piece == 'P' and end_row == start_row-2:
        new_gs.ep_flag_array[0][start_col] = True
    elif piece == 'p' and end_row == start_row+2:
        new_gs.ep_flag_array[1][start_col] = True
    elif piece == 'K':
        new_gs.wking_moved_flag = True
    elif piece == 'k':
        new_gs.bking_moved_flag = True
    if piece.isupper():
        new_gs.white_to_move_flag = False
    else:
        new_gs.white_to_move_flag = True
    return new_gs

def make_enpassant_move(gs, start_row, start_col, column, player):
    new_gs = copy.deepcopy(gs)
    new_gs.board[start_row][start_col] = '-'
    new_gs.board[start_row][column] = '-'
    if player == 'white':
        new_gs.board[start_row-1][column] = 'P'
        new_gs.white_to_move_flag = False
    else:
        new_gs.board[start_row+1][column] = 'p'
        new_gs.white_to_move_flag = True
        
    return new_gs

def castle(gs, side, player):
    if player == 'white':
        new_gs = copy.deepcopy(gs)
        new_gs.board[7][4] = '-'
        new_gs.white_to_move_flag = False
        if side == 'right':
            new_gs.board[7][7] = '-'
            new_gs.board[7][6] = 'K'
            new_gs.board[7][5] = 'R'
        else:
            new_gs.board[7][0] = '-'
            new_gs.board[7][1] = '-'
            new_gs.board[7][2] = 'K'
            new_gs.board[7][3] = 'R'

        if not is_white_in_check(new_gs):
            new_gs.wking_moved_flag = True
            return new_gs
    else:
        new_gs = copy.deepcopy(gs)
        new_gs.board[0][4] = '-'
        new_gs.white_to_move_flag = True
        if side == 'right':
            new_gs.board[0][7] = '-'
            new_gs.board[0][6] = 'k'
            new_gs.board[0][5] = 'r'
        else:
            new_gs.board[0][0] = '-'
            new_gs.board[0][1] = '-'
            new_gs.board[0][2] = 'k'
            new_gs.board[0][3] = 'r'
    
        if not is_black_in_check(new_gs):
            new_gs.bking_moved_flag = True
            return new_gs
        
    return False

def generate_pawn_moves(gs, i, j, player):
    moves = []

    if player == 'white':
        if i-1 >= 0 and gs.board[i-1][j] == '-':
            moves.append(make_move(gs, i, j, i-1, j, 'P'))
            if i == 6 and gs.board[i-2][j] == '-':
                moves.append(make_move(gs, i, j, i-2, j, 'P'))
        if i-1 >= 0 and j-1 >= 0 and gs.board[i-1][j-1].islower():
            moves.append(make_move(gs, i, j, i-1, j-1, 'P'))
        if j-1 >= 0 and gs.board[i-1][j-1] == '-' and i == 3 and gs.ep_flag_array[1][j-1] == True:
            moves.append(make_enpassant_move(gs, i, j, j-1, player))
        if i-1 >= 0 and j+1 <= 7 and gs.board[i-1][j+1].islower():
            moves.append(make_move(gs, i, j, i-1, j+1, 'P'))
        if j+1 <= 7 and gs.board[i-1][j+1] == '-' and i == 3 and gs.ep_flag_array[1][j+1] == True:
            moves.append(make_enpassant_move(gs, i, j, j+1, player))

    else:
        if i+1 <= 7 and gs.board[i+1][j] == '-':
            moves.append(make_move(gs, i, j, i+1, j, 'p'))
            if i == 1 and gs.board[i+2][j] == '-':
                moves.append(make_move(gs, i, j, i+2, j, 'p'))
        if i+1 <= 7 and j-1 >= 0 and gs.board[i+1][j-1].isupper():
            moves.append(make_move(gs, i, j, i+1, j-1, 'p'))
        if j-1 >= 0 and gs.board[i+1][j-1] == '-' and i == 4 and gs.ep_flag_array[0][j-1] == True:
            moves.append(make_enpassant_move(gs, i, j, j-1, player))
        if i+1 <= 7 and j+1 <= 7 and gs.board[i+1][j+1].isupper():
            moves.append(make_move(gs, i, j, i+1, j+1, 'p'))
        if j+1 <= 7 and gs.board[i+1][j+1] == '-' and i == 4 and gs.ep_flag_array[0][j+1] == True:
            moves.append(make_enpassant_move(gs, i, j, j+1, player))

    return moves 

def generate_sliding_moves(gs, i, j, player):
    moves = []
    
    if player == 'white':
        if gs.board[i][j] != 'B':
            multiple = 1
            while i+multiple <= 7 and not gs.board[i+multiple][j].isupper(): 
                moves.append(make_move(gs, i, j, i+multiple, j, gs.board[i][j]))
                if gs.board[i+multiple][j].islower():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i-multiple >= 0 and not gs.board[i-multiple][j].isupper():
                moves.append(make_move(gs, i, j, i-multiple, j, gs.board[i][j]))
                if gs.board[i-multiple][j].islower():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while j+multiple <= 7 and not gs.board[i][j+multiple].isupper():
                moves.append(make_move(gs, i, j, i, j+multiple, gs.board[i][j]))
                if gs.board[i][j+multiple].islower():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while j-multiple >= 0 and not gs.board[i][j-multiple].isupper():
                moves.append(make_move(gs, i, j, i, j-multiple, gs.board[i][j]))
                if gs.board[i][j-multiple].islower():
                    multiple += 10
                else:
                    multiple += 1

        if gs.board[i][j] != 'R':
            multiple = 1
            while i+multiple <= 7 and j+multiple <= 7 and not gs.board[i+multiple][j+multiple].isupper():
                moves.append(make_move(gs, i, j, i+multiple, j+multiple, gs.board[i][j]))
                if gs.board[i+multiple][j+multiple].islower():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i+multiple <= 7 and j-multiple >= 0 and not gs.board[i+multiple][j-multiple].isupper():
                moves.append(make_move(gs, i, j, i+multiple, j-multiple, gs.board[i][j]))
                if gs.board[i+multiple][j-multiple].islower():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i-multiple >= 0 and j+multiple <= 7 and not gs.board[i-multiple][j+multiple].isupper():
                moves.append(make_move(gs, i, j, i-multiple, j+multiple, gs.board[i][j]))
                if gs.board[i-multiple][j+multiple].islower():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i-multiple >= 0 and j-multiple >= 0 and not gs.board[i-multiple][j-multiple].isupper():
                moves.append(make_move(gs, i, j, i-multiple, j-multiple, gs.board[i][j]))
                if gs.board[i-multiple][j-multiple].islower():
                    multiple += 10
                else:
                    multiple += 1

    else:
        if gs.board[i][j] != 'b':
            multiple = 1
            while i+multiple <= 7 and not gs.board[i+multiple][j].islower(): 
                moves.append(make_move(gs, i, j, i+multiple, j, gs.board[i][j]))
                if gs.board[i+multiple][j].isupper():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i-multiple >= 0 and not gs.board[i-multiple][j].islower():
                moves.append(make_move(gs, i, j, i-multiple, j, gs.board[i][j]))
                if gs.board[i-multiple][j].isupper():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while j+multiple <= 7 and not gs.board[i][j+multiple].islower():
                moves.append(make_move(gs, i, j, i, j+multiple, gs.board[i][j]))
                if gs.board[i][j+multiple].isupper():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while j-multiple >= 0 and not gs.board[i][j-multiple].islower():
                moves.append(make_move(gs, i, j, i, j-multiple, gs.board[i][j]))
                if gs.board[i][j-multiple].isupper():
                    multiple += 10
                else:
                    multiple += 1

        if gs.board[i][j] != 'r':
            multiple = 1
            while i+multiple <= 7 and j+multiple <= 7 and not gs.board[i+multiple][j+multiple].islower():
                moves.append(make_move(gs, i, j, i+multiple, j+multiple, gs.board[i][j]))
                if gs.board[i+multiple][j+multiple].isupper():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i+multiple <= 7 and j-multiple >= 0 and not gs.board[i+multiple][j-multiple].islower():
                moves.append(make_move(gs, i, j, i+multiple, j-multiple, gs.board[i][j]))
                if gs.board[i+multiple][j-multiple].isupper():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i-multiple >= 0 and j+multiple <= 7 and not gs.board[i-multiple][j+multiple].islower():
                moves.append(make_move(gs, i, j, i-multiple, j+multiple, gs.board[i][j]))
                if gs.board[i-multiple][j+multiple].isupper():
                    multiple += 10
                else:
                    multiple += 1

            multiple = 1
            while i-multiple >= 0 and j-multiple >= 0 and not gs.board[i-multiple][j-multiple].islower():
                moves.append(make_move(gs, i, j, i-multiple, j-multiple, gs.board[i][j]))
                if gs.board[i-multiple][j-multiple].isupper():
                    multiple += 10
                else:
                    multiple += 1
    return moves
        
def generate_knight_moves(gs, i, j, player):
    moves = []
    
    if player == 'white':
        if i+1 <= 7 and j+2 <= 7 and not gs.board[i+1][j+2].isupper():
            moves.append(make_move(gs, i, j, i+1, j+2, 'N'))
        if i+1 <= 7 and j-2 >= 0 and not gs.board[i+1][j-2].isupper():
            moves.append(make_move(gs, i, j, i+1, j-2, 'N'))
        if i-1 >= 0 and j+2 <= 7 and not gs.board[i-1][j+2].isupper():
            moves.append(make_move(gs, i, j, i-1, j+2, 'N'))
        if i-1 >= 0 and j-2 >= 0 and not gs.board[i-1][j-2].isupper():
            moves.append(make_move(gs, i, j, i-1, j-2, 'N'))
        if i+2 <= 7 and j+1 <= 7 and not gs.board[i+2][j+1].isupper():
            moves.append(make_move(gs, i, j, i+2, j+1, 'N'))
        if i+2 <= 7 and j-1 >= 0 and not gs.board[i+2][j-1].isupper():
            moves.append(make_move(gs, i, j, i+2, j-1, 'N'))
        if i-2 >= 0 and j+1 <= 7 and not gs.board[i-2][j+1].isupper():
            moves.append(make_move(gs, i, j, i-2, j+1, 'N'))
        if i-2 >= 0 and j-1 >= 0 and not gs.board[i-2][j-1].isupper():
            moves.append(make_move(gs, i, j, i-2, j-1, 'N'))
    else:
        if i+1 <= 7 and j+2 <= 7 and not gs.board[i+1][j+2].islower():
            moves.append(make_move(gs, i, j, i+1, j+2, 'n'))
        if i+1 <= 7 and j-2 >= 0 and not gs.board[i+1][j-2].islower():
            moves.append(make_move(gs, i, j, i+1, j-2, 'n'))
        if i-1 >= 0 and j+2 <= 7 and not gs.board[i-1][j+2].islower():
            moves.append(make_move(gs, i, j, i-1, j+2, 'n'))
        if i-1 >= 0 and j-2 >= 0 and not gs.board[i-1][j-2].islower():
            moves.append(make_move(gs, i, j, i-1, j-2, 'n'))
        if i+2 <= 7 and j+1 <= 7 and not gs.board[i+2][j+1].islower():
            moves.append(make_move(gs, i, j, i+2, j+1, 'n'))
        if i+2 <= 7 and j-1 >= 0 and not gs.board[i+2][j-1].islower():
            moves.append(make_move(gs, i, j, i+2, j-1, 'n'))
        if i-2 >= 0 and j+1 <= 7 and not gs.board[i-2][j+1].islower():
            moves.append(make_move(gs, i, j, i-2, j+1, 'n'))
        if i-2 >= 0 and j-1 >= 0 and not gs.board[i-2][j-1].islower():
            moves.append(make_move(gs, i, j, i-2, j-1, 'n'))

    return moves

def generate_king_moves(gs, i, j, player):
    moves = []
    
    if player == 'white':
        if i+1 <= 7 and not gs.board[i+1][j].isupper():
            moves.append(make_move(gs, i, j, i+1, j, 'K'))
        if i-1 >= 0 and not gs.board[i-1][j].isupper():
            moves.append(make_move(gs, i, j, i-1, j, 'K'))
        if j+1 <= 7 and not gs.board[i][j+1].isupper():
            moves.append(make_move(gs, i, j, i, j+1, 'K'))
        if j-1 >= 0 and not gs.board[i][j-1].isupper():
            moves.append(make_move(gs, i, j, i, j-1, 'K'))
        if i+1 <= 7 and j+1 <= 7 and not gs.board[i+1][j+1].isupper():
            moves.append(make_move(gs, i, j, i+1, j+1, 'K'))
        if i+1 <= 7 and j-1 >= 0 and not gs.board[i+1][j-1].isupper():
            moves.append(make_move(gs, i, j, i+1, j-1, 'K'))
        if i-1 >= 0 and j+1 <= 7 and not gs.board[i-1][j+1].isupper():
            moves.append(make_move(gs, i, j, i-1, j+1, 'K'))
        if i-1 >= 0 and j-1 >= 0 and not gs.board[i-1][j-1].isupper():
            moves.append(make_move(gs, i, j, i-1, j-1, 'K'))
        if not gs.wking_moved_flag:
            if not gs.wrrook_moved_flag and gs.board[7][5] == '-' and gs.board[7][6] == '-':
                val = castle(gs, 'right', player)
                if val:
                    moves.append(val)
            if not gs.wlrook_moved_flag and gs.board[7][1] == '-' and gs.board[7][2] == '-' and gs.board[7][3] == '-':
                val = castle(gs, 'left', player)
                if val:
                    moves.append(val)

    else:
        if i+1 <= 7 and not gs.board[i+1][j].islower():
            moves.append(make_move(gs, i, j, i+1, j, 'k'))
        if i-1 >= 0 and not gs.board[i-1][j].islower():
            moves.append(make_move(gs, i, j, i-1, j, 'k'))
        if j+1 <= 7 and not gs.board[i][j+1].islower():
            moves.append(make_move(gs, i, j, i, j+1, 'k'))
        if j-1 >= 0 and not gs.board[i][j-1].islower():
            moves.append(make_move(gs, i, j, i, j-1, 'k'))
        if i+1 <= 7 and j+1 <= 7 and not gs.board[i+1][j+1].islower():
            moves.append(make_move(gs, i, j, i+1, j+1, 'k'))
        if i+1 <= 7 and j-1 >= 0 and not gs.board[i+1][j-1].islower():
            moves.append(make_move(gs, i, j, i+1, j-1, 'k'))
        if i-1 >= 0 and j+1 <= 7 and not gs.board[i-1][j+1].islower():
            moves.append(make_move(gs, i, j, i-1, j+1, 'k'))
        if i-1 >= 0 and j-1 >= 0 and not gs.board[i-1][j-1].islower():
            moves.append(make_move(gs, i, j, i-1, j-1, 'k'))
        if not gs.bking_moved_flag:
            if not gs.brrook_moved_flag and gs.board[0][5] == '-' and gs.board[0][6] == '-':
                val = castle(gs, 'right', player)
                if val:
                    moves.append(val)
            if not gs.blrook_moved_flag and gs.board[0][1] == '-' and gs.board[0][2] == '-' and gs.board[0][3] == '-':
                val = castle(gs, 'left', player)
                if val:
                    moves.append(val)
    return moves

def all_white_moves(gs, bool=True):
    moves = []
    for i in range(len(gs.board)):
        for j in range(len(gs.board[i])):
            if gs.board[i][j].isupper():
                if gs.board[i][j] == 'P':
                    moves.extend(generate_pawn_moves(gs, i, j, 'white'))
                elif gs.board[i][j] == 'R' or gs.board[i][j] == 'B' or gs.board[i][j] == 'Q':
                    moves.extend(generate_sliding_moves(gs, i, j, 'white'))
                elif gs.board[i][j] == 'N':
                    moves.extend(generate_knight_moves(gs, i, j, 'white'))
                else:
                    moves.extend(generate_king_moves(gs, i, j, 'white'))

    if bool:
        moves = [ele for ele in moves if not is_white_in_check(ele)]

    return moves

def all_black_moves(gs, bool=True):
    moves = []
    for i in range(len(gs.board)):
        for j in range(len(gs.board[i])):
            if gs.board[i][j].islower():
                if gs.board[i][j] == 'p':
                    moves.extend(generate_pawn_moves(gs, i, j, 'black'))
                elif gs.board[i][j] == 'r' or gs.board[i][j] == 'b' or gs.board[i][j] == 'q':
                    moves.extend(generate_sliding_moves(gs, i, j, 'black'))
                elif gs.board[i][j] == 'n':
                    moves.extend(generate_knight_moves(gs, i, j, 'black'))
                else:
                    moves.extend(generate_king_moves(gs, i, j, 'black'))

    if bool:
        moves = [ele for ele in moves if not is_black_in_check(ele)]

    return moves
