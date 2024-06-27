from data.positional_values import *
from classes.gamestate import *

piece_points = {'p': 100, 'r': 500, 'b': 315, 'n': 300, 'q': 900}

def minimax(gs: Gamestate, depth, alpha, beta, white_to_move) -> tuple[int, Gamestate]:
    if depth == 0:
        return evaluate(gs)
    if white_to_move:
        max_eval = -999999
        best_move = None
        if not gs.processed:
            gs.generate_all_moves()
        for e in gs.possible_moves:
            eval_score, _ = minimax(e, depth-1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = e
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 999999
        best_move = None
        if not gs.processed:
            gs.generate_all_moves()
        for e in gs.possible_moves:
            eval_score, _ = minimax(e, depth-1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = e
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move
    
def evaluate(gs: Gamestate) -> tuple[int, Gamestate]:
    if gs.is_checkmate():
        if gs.is_white_to_move:
            return -999999, gs
        else:
            return 999999, gs
    points_white = 0
    points_black = 0

    for row_idx, row in enumerate(gs.board.matrix):
        for col_idx, piece in enumerate(row):
            if piece != '-' and piece.lower() != 'k':
                if piece.isupper():  # White piece
                    piece_value = piece_points[piece.lower()]
                    positional_value = (gs.pieces / 32) * positional_value_dict[piece.lower()][0][row_idx][col_idx] + \
                                       (1 - gs.pieces / 32) * positional_value_dict[piece.lower()][1][row_idx][col_idx]
                    points_white += piece_value + positional_value
                else:  # Black piece
                    piece_value = piece_points[piece]
                    positional_value = (gs.pieces / 32) * positional_value_dict[piece][0][7-row_idx][7-col_idx] + \
                                       (1 - gs.pieces / 32) * positional_value_dict[piece][1][7-row_idx][7-col_idx]
                    points_black += piece_value + positional_value

    return points_white - points_black, gs