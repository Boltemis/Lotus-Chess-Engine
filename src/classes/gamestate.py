from typing import List
from utils import *

class Gamestate:
    def __init__(self, board=None, flags=None):
        if board:
            self.board: List[List][str] = board
        else:
            self.board: List[List][str] = [
                                            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                                            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                                            ['-', '-', '-', '-', '-', '-', '-', '-'], 
                                            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
                                            ]
        
        if flags:
            self.flags = flags
        else:
            self.flags: dict[str: bool|int] = {
                                            "white_king_moved": False, 
                                            "left_white_rook_moved": False, 
                                            "right_white_rook_moved": False, 
                                            "black_king_moved": False,
                                            "left_black_rook_moved": False, 
                                            "right_black_rook_moved": False, 
                                            "white_to_move": True,
                                            "pieces_counter": 32,
                                            "fifty_move_counter": 0,
                                            "threefold_repetition_counter": 0
                                            }

    def copy(self, board: List[List[str]]) -> 'Gamestate':
        flags_copy = {key: value for key, value in self.flags.items()}
        copy = Gamestate(board, flags_copy)
        return copy

    def change_player(self) -> None:
        self.flags["white_to_move"] = not self.flags["white_to_move"]

    def is_white_to_move(self) -> bool:
        return self.flags["white_to_move"]
    
    def get_pieces_counter(self) -> int:
        return self.flags["pieces_counter"]

    def is_check(self) -> bool:
        if self.is_white_to_move():
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'K':
                        return self.is_square_under_attack(i, j)
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'k':
                        return self.is_square_under_attack(i, j)

    def is_checkmate(self) -> bool: # should use this generate_all_moves call for the next iteration
        return self.is_check() and not self.generate_all_moves(self.is_white_to_move())

    def is_stalemate(self) -> bool:
        return self.is_stalemate_by_no_moves() or self.is_stalemate_by_fifty_move_rule() or self.is_stalemate_by_insufficient_material() or self.is_stalemate_by_threefold_repetition()
    
    def is_stalemate_by_no_moves(self) -> bool: # should use this generate_all_moves call for the next iteration
        return not self.is_check() and not self.generate_all_moves(self.is_white_to_move())

    def is_stalemate_by_insufficient_material(self) -> bool:
        return False

    def is_stalemate_by_threefold_repetition(self) -> bool:
        return False

    def is_stalemate_by_fifty_move_rule(self) -> bool:
        return False

    def is_valid_move(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        piece = self.board[start_row][start_col]
        destination_piece = self.board[end_row][end_col]

        def is_empty_or_opponent_piece(row, col):
            return self.board[row][col] == '-' or (piece.isupper() != self.board[row][col].isupper())

        if piece.lower() == 'p':
            if start_col == end_col:
                if piece.isupper():
                    if start_row == 6:
                        return end_row == start_row - 1 or (end_row == start_row - 2 and self.board[end_row + 1][end_col] == '-')
                    else:
                        return end_row == start_row - 1
                else:
                    if start_row == 1:
                        return end_row == start_row + 1 or (end_row == start_row + 2 and self.board[end_row - 1][end_col] == '-')
                    else:
                        return end_row == start_row + 1
            elif abs(end_col - start_col) == 1 and destination_piece != '-':
                return is_empty_or_opponent_piece(end_row, end_col) and ((piece.isupper() and end_row == start_row - 1) or (not piece.isupper() and end_row == start_row + 1))
            else:
                return False
        elif piece.lower() == 'n':
            return (abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1) or (abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2)
        elif piece.lower() == 'b':
            return abs(end_row - start_row) == abs(end_col - start_col) and all(is_empty_or_opponent_piece(r, c) for r, c in zip(range(start_row, end_row, 1 if end_row > start_row else -1), range(start_col, end_col, 1 if end_col > start_col else -1)))
        elif piece.lower() == 'r':
            return (start_row == end_row or start_col == end_col) and all(is_empty_or_opponent_piece(r, c) for r, c in ((r, start_col) if start_row == end_row else (start_row, c) for r, c in zip(range(min(start_row, end_row), max(start_row, end_row)), range(min(start_col, end_col), max(start_col, end_col)))))
        elif piece.lower() == 'q':
            return (start_row == end_row or start_col == end_col or abs(end_row - start_row) == abs(end_col - start_col)) and all(is_empty_or_opponent_piece(r, c) for r, c in ((r, start_col) if start_row == end_row else (start_row, c) if start_col == end_col else (r, c) for r, c in zip(range(min(start_row, end_row), max(start_row, end_row)), range(min(start_col, end_col), max(start_col, end_col)))))
        elif piece.lower() == 'k':
            return abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1
        else:
            return False

    def is_square_under_attack(self, row, col) -> bool:
        if self.is_white_to_move():
            for r in range(8):
                for c in range(8):
                    piece = self.board[r][c]
                    if piece.islower():
                        if self.is_valid_move(r, c, row, col):
                            return True
            return False
    
        else:
            for r in range(8):
                for c in range(8):
                    piece = self.board[r][c]
                    if piece.isupper():
                        if self.is_valid_move(r, c, row, col):
                            return True
            return False

    def generate_pawn_moves(self, row: int, col: int) -> List['Gamestate']:
        moves = []
        if self.board[row][col] == "P":
            if row-1 > 0 and self.board[row-1][col] == "-":
                new_move = [ele[:] for ele in self.board]
                new_move[row-1][col] = "P"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
            if row-1 > 0 and col-1 > 0 and self.board[row-1][col-1].islower():
                new_move = [ele[:] for ele in self.board]
                new_move[row-1][col-1] = "P"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
            if row-1 > 0 and col+1 < 8 and self.board[row-1][col+1].islower():
                new_move = [ele[:] for ele in self.board]
                new_move[row-1][col+1] = "P"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
            if row == 6 and self.board[row-2][col] == "-":
                new_move = [ele[:] for ele in self.board]
                new_move[row-2][col] = "P"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
        else:
            if row+1 < 8 and self.board[row+1][col] == "-":
                new_move = [ele[:] for ele in self.board]
                new_move[row+1][col] = "p"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
            if row+1 < 8 and col-1 > 0 and self.board[row+1][col-1].isupper():
                new_move = [ele[:] for ele in self.board]
                new_move[row+1][col-1] = "p"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
            if row+1 < 8 and col+1 < 8 and self.board[row+1][col+1].isupper():
                new_move = [ele[:] for ele in self.board]
                new_move[row+1][col+1] = "p"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)
            if row == 1 and self.board[row+2][col] == "-":
                new_move = [ele[:] for ele in self.board]
                new_move[row+2][col] = "p"
                new_move[row][col] = "-"
                new_gamestate = self.copy(new_move)
                
                if not new_gamestate.is_check():
                    new_gamestate.change_player()
                    moves.append(new_gamestate)

        return moves

    def generate_bishop_moves(self, row: int, col: int) -> List['Gamestate']:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for step in range(1, 8):
                new_row, new_col = row + dr * step, col + dc * step
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] == "-" or (self.board[row][col].isupper() != self.board[new_row][new_col].isupper()):
                        new_move = [row[:] for row in self.board]
                        new_move[new_row][new_col] = self.board[row][col]
                        new_move[row][col] = "-"
                        new_gamestate = self.copy(new_move)
                        
                        if not new_gamestate.is_check():
                            new_gamestate.change_player()
                            moves.append(new_gamestate)
                    if self.board[new_row][new_col] != "-":
                        break
                else:
                    break 

        return moves

    def generate_rook_moves(self, row: int, col: int) -> List['Gamestate']:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for step in range(1, 8):
                new_row, new_col = row + dr * step, col + dc * step
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] == "-" or (self.board[row][col].isupper() != self.board[new_row][new_col].isupper()):
                        new_move = [row[:] for row in self.board]
                        new_move[new_row][new_col] = self.board[row][col]
                        new_move[row][col] = "-"
                        new_gamestate = self.copy(new_move)
                        
                        if not new_gamestate.is_check():
                            new_gamestate.change_player()
                            moves.append(new_gamestate)
                    if self.board[new_row][new_col] != "-":
                        break
                else:
                    break

        return moves

    def generate_queen_moves(self, row: int, col: int) -> List['Gamestate']:
        moves = self.generate_rook_moves(row, col) + self.generate_bishop_moves(row, col)
        return moves

    def generate_king_moves(self, row: int, col: int) -> List['Gamestate']:
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == "-" or (self.board[row][col].isupper() != self.board[new_row][new_col].isupper()):
                    new_move = [row[:] for row in self.board]
                    new_move[new_row][new_col] = self.board[row][col]
                    new_move[row][col] = "-"
                    new_gamestate = self.copy(new_move)
                    
                    if not new_gamestate.is_check():
                        new_gamestate.change_player()
                        moves.append(new_gamestate)

        return moves
            
    def generate_knight_moves(self, row: int, col: int) -> List['Gamestate']:
        moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == "-" or (self.board[row][col].isupper() != self.board[new_row][new_col].isupper()):
                    new_move = [row[:] for row in self.board]
                    new_move[new_row][new_col] = self.board[row][col]
                    new_move[row][col] = "-"
                    new_gamestate = self.copy(new_move)
                    
                    if not new_gamestate.is_check():
                        new_gamestate.change_player()
                        moves.append(new_gamestate)

        return moves

    def generate_all_moves(self, player_is_white) -> List['Gamestate']:
        moves = []
        if player_is_white:
            for i in range(8):
                for j in range(8):
                    match self.board[i][j]:
                        case "P":
                            moves.extend(self.generate_pawn_moves(i, j))
                        case "Q":
                            moves.extend(self.generate_queen_moves(i, j))
                        case "N":
                            moves.extend(self.generate_knight_moves(i, j))
                        case "B":
                            moves.extend(self.generate_bishop_moves(i, j))
                        case "R":
                            moves.extend(self.generate_rook_moves(i, j))
                        case "K":
                            moves.extend(self.generate_king_moves(i, j))
                        case _:
                            pass
        else:
            for i in range(8):
                for j in range(8):
                    match self.board[i][j]:
                        case "p":
                            moves.extend(self.generate_pawn_moves(i, j))
                        case "q":
                            moves.extend(self.generate_queen_moves(i, j))
                        case "n":
                            moves.extend(self.generate_knight_moves(i, j))
                        case "b":
                            moves.extend(self.generate_bishop_moves(i, j))
                        case "r":
                            moves.extend(self.generate_rook_moves(i, j))
                        case "k":
                            moves.extend(self.generate_king_moves(i, j))
                        case _:
                            pass
        
        return moves