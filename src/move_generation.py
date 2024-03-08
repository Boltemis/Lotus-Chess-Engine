from classes.gamestate import *
from playermode import *

def generate_pawn_moves(gs: Gamestate, row: int, col: int) -> List[Gamestate]:
    moves = []
    if gs.board[row][col] == "P":
        if gs.board[row-1][col] == "-":
            new_move = [ele[:] for ele in gs.board]
            new_move[row-1][col] = "P"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
            moves.append(new_gamestate)
        if row-1 > 0 and col-1 > 0 and gs.board[row-1][col-1].islower():
            new_move = [ele[:] for ele in gs.board]
            new_move[row-1][col-1] = "P"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
            moves.append(new_gamestate)
        if row-1 > 0 and col+1 < 8 and gs.board[row-1][col+1].islower():
            new_move = [ele[:] for ele in gs.board]
            new_move[row-1][col+1] = "P"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
        if row == 6 and gs.board[row-2][col] == "-":
            new_move = [ele[:] for ele in gs.board]
            new_move[row-2][col] = "P"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
            moves.append(new_gamestate)
    else:
        if gs.board[row+1][col] == "-":
            new_move = [ele[:] for ele in gs.board]
            new_move[row+1][col] = "p"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
            moves.append(new_gamestate)
        if row+1 < 8 and col-1 > 0 and gs.board[row+1][col-1].isupper():
            new_move = [ele[:] for ele in gs.board]
            new_move[row+1][col-1] = "p"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
            moves.append(new_gamestate)
        if row+1 < 8 and col+1 < 8 and gs.board[row+1][col+1].isupper():
            new_move = [ele[:] for ele in gs.board]
            new_move[row+1][col+1] = "p"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
        if row == 1 and gs.board[row+2][col] == "-":
            new_move = [ele[:] for ele in gs.board]
            new_move[row-2][col] = "p"
            new_move[row][col] = "-"
            new_gamestate = gs.copy(new_move)
            moves.append(new_gamestate)

    return moves

def generate_bishop_moves(gs: Gamestate, row: int, col: int) -> List[Gamestate]:
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        for step in range(1, 8):
            new_row, new_col = row + dr * step, col + dc * step
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if gs.board[new_row][new_col] == "-" or (gs.board[row][col].isupper() != gs.board[new_row][new_col].isupper()):
                    new_board = [row[:] for row in gs.board]
                    new_board[new_row][new_col] = gs.board[row][col]
                    new_board[row][col] = "-"
                    moves.append(Gamestate(new_board))
                if gs.board[new_row][new_col] != "-":
                    break
            else:
                break 

    return moves

def generate_rook_moves(gs: Gamestate, row: int, col: int) -> List[Gamestate]:
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        for step in range(1, 8):
            new_row, new_col = row + dr * step, col + dc * step
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if gs.board[new_row][new_col] == "-" or (gs.board[row][col].isupper() != gs.board[new_row][new_col].isupper()):
                    new_board = [row[:] for row in gs.board]
                    new_board[new_row][new_col] = gs.board[row][col]
                    new_board[row][col] = "-"
                    moves.append(Gamestate(new_board))
                if gs.board[new_row][new_col] != "-":
                    break
            else:
                break

    return moves

def generate_queen_moves(gs: Gamestate, row: int, col: int) -> List[Gamestate]:
    moves = generate_rook_moves(gs, row, col) + generate_bishop_moves(gs, row, col)
    return moves

def generate_king_moves(gs: Gamestate, row: int, col: int) -> List[Gamestate]:
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if gs.board[new_row][new_col] == "-" or (gs.board[row][col].isupper() != gs.board[new_row][new_col].isupper()):
                new_board = [row[:] for row in gs.board]
                new_board[new_row][new_col] = gs.board[row][col]
                new_board[row][col] = "-"
                moves.append(Gamestate(new_board))

    return moves
        
def generate_knight_moves(gs: Gamestate, row: int, col: int) -> List[Gamestate]:
    moves = []
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if gs.board[new_row][new_col] == "-" or (gs.board[row][col].isupper() != gs.board[new_row][new_col].isupper()):
                new_board = [row[:] for row in gs.board]
                new_board[new_row][new_col] = gs.board[row][col]
                new_board[row][col] = "-"
                moves.append(Gamestate(new_board))

    return moves

def generate_all_moves(gs, player_is_white) -> List[Gamestate]:
    moves = []
    if player_is_white:
        for i in range(8):
            for j in range(8):
                match gs.board[i][j]:
                    case "P":
                        moves.extend(generate_pawn_moves(gs, i, j))
                    case "Q":
                        moves.extend(generate_queen_moves(gs, i, j))
                    case "N":
                        moves.extend(generate_knight_moves(gs, i, j))
                    case "B":
                        moves.extend(generate_bishop_moves(gs, i, j))
                    case "R":
                        moves.extend(generate_rook_moves(gs, i, j))
                    case "K":
                        moves.extend(generate_king_moves(gs, i, j))
                    case _:
                        pass
    else:
        for i in range(8):
            for j in range(8):
                match gs.board[i][j]:
                    case "p":
                        moves.extend(generate_pawn_moves(gs, i, j))
                    case "q":
                        moves.extend(generate_queen_moves(gs, i, j))
                    case "n":
                        moves.extend(generate_knight_moves(gs, i, j))
                    case "b":
                        moves.extend(generate_bishop_moves(gs, i, j))
                    case "r":
                        moves.extend(generate_rook_moves(gs, i, j))
                    case "k":
                        moves.extend(generate_king_moves(gs, i, j))
                    case _:
                        pass
    
    return moves