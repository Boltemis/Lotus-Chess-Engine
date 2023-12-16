import sys
from move import *

piece_points = {'p': 1.000, 'r': 5.000, 'b': 3.150, 'n': 3.000, 'q': 9.000}
                
def minimax(board, depth, beta, player):
    if depth == 0:
        return board
    if player == 'White':
        max_eval = -sys.maxsize - 1
        arr = all_white_moves(board)
        for e in arr:
            eval = minimax(e, depth-1, alpha, beta, "Black")
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = sys.maxsize
        arr = all_black_moves(board)
        for e in arr:
            eval = minimax(e, depth-1, alpha, beta, "White")
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
def eval(gs):
    points_white = 0
    points_black = 0

    for row in gs.board:
        for piece in row:
            if piece != '-' and piece.lower() != 'k':
                if piece.isupper():
                    points_white += piece_points[(piece).lower()]
                else:
                    points_black += piece_points[(piece).lower()]
    
    return points_white-points_black