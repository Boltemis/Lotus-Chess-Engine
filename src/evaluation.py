from data.positional_values import *
from classes.gamestate import *

piece_points = {'p': 100, 'r': 500, 'b': 315, 'n': 300, 'q': 900}

def minimax(gs: Gamestate, depth, alpha, beta, player_is_white) -> tuple[int, Gamestate]:
    if depth == 0:
        return evaluate(gs)
    
    if player_is_white:
        max_eval = -999999
        best_move = None
        if not gs.processed:
            gs.generate_all_moves()
        for e in gs.possible_moves:
            new_gs = gs.apply_move(e)
            eval_score, _ = minimax(new_gs, depth-1, alpha, beta, "Black")
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = new_gs
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 999999
        best_move = None
        for e in gs.possible_moves:
            new_gs = gs.apply_move(e)
            eval_score, _ = minimax(new_gs, depth-1, alpha, beta, "White")
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = e
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, new_gs
    
def evaluate(gs: Gamestate) -> tuple[int, Gamestate]:
    #if gs.is_checkmate():
     #   if gs.is_white_to_move:
      #      return 999999, gs
       # else:
        #    return -999999, gs
    points_white = 0
    points_black = 0

    for row_idx, row in enumerate(gs.board.matrix):
        for col_idx, piece in enumerate(row):
            if piece != '-' and piece.lower() != 'k':
                if piece.isupper():
                    points_white += (piece_points[piece.lower()])
                    +(gs.pieces/32)*(positional_value_dict[piece.lower()][0][row_idx][col_idx])
                    +(1-(gs.pieces/32))*(positional_value_dict[piece.lower()][1][row_idx][col_idx])
                else:
                    points_black += (piece_points[piece])
                    +(gs.pieces/32)*(positional_value_dict[piece][0][7-row_idx][7-col_idx])
                    +(1-(gs.pieces/32))*(positional_value_dict[piece][1][7-row_idx][7-col_idx])
    
    return points_white-points_black, gs