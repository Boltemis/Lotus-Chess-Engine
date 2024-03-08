import sys
from move import *
from positional_value_db import *

piece_points = {'p': 100, 'r': 500, 'b': 315, 'n': 300, 'q': 900, 'k': 5000}

def minimax(board, depth, alpha, beta, player):
    if depth == 0:
        return evaluate(board)
    if player == 'White':
        max_eval = -999999
        arr = all_white_moves(board)
        best_move = None
        for e in arr:
            eval_score, _ = minimax(e, depth-1, alpha, beta, "Black")
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = e
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 999999
        arr = all_black_moves(board)
        best_move = None
        for e in arr:
            eval_score, _ = minimax(e, depth-1, alpha, beta, "White")
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = e
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move
    
def evaluate(gs):
    if is_checkmate(gs):
        if gs.white_to_move_flag:
            return 999999, gs
        else:
            return -999999, gs
    points_white = 0
    points_black = 0

    for row_idx, row in enumerate(gs.board):
        for col_idx, piece in enumerate(row):
            if piece != '-':
                if piece.isupper():
                    if gs.amount_of_pieces >= 12: # midgame
                        points_white += (piece_points[piece.lower()])+(positional_value_dict[piece.lower()][0][row_idx][col_idx])
                    else: # endgame
                        points_white += (piece_points[piece.lower()])+(positional_value_dict[piece.lower()][1][row_idx][col_idx])
                else:
                    if gs.amount_of_pieces >= 12: # midgame
                        points_black += (piece_points[piece])+(positional_value_dict[piece][0][7-row_idx][7-col_idx])
                    else: # endgame
                        points_black += (piece_points[piece])+(positional_value_dict[piece][1][7-row_idx][7-col_idx])
    
    return points_white-points_black, gs