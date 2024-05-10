from typing import List

from classes.board import *
from classes.move import *

class Gamestate:
    def __init__(self, board: 'Board', flags: dict[str: bool], sm_counter: int, pieces: int, threefold: int):
        self.board = board
        self.flags = flags
        self.sm_counter = sm_counter
        self.pieces = pieces
        self.threefold = threefold
        self.possible_moves = []
        self.processed = False

    def copy(self) -> 'Gamestate':
        """ Returns an exact copy of the gamestate"""
        flags_copy = {key: value for key, value in self.flags.items()}
        copy = Gamestate(self.board, flags_copy, self.sm_counter, self.pieces, self.threefold)
        return copy

    def apply_move(self, move: 'Move') -> 'Gamestate':
        # ADD ROOK AND KING FLAGS
        """ Applies a move to a gamestate and returns a new instance of Gamestate with the move applied """
        gs = self.copy()
        piece = gs.board.matrix[move.start_row][move.start_col]
        gs.board.matrix[move.start_row][move.start_col] = '-'
        gs.board.matrix[move.end_row][move.end_col] = piece

        if piece.lower() == 'k':
            if move.end_col == move.start_col + 2: # Castling short
                gs.board.matrix[move.start_row][move.start_row+3] = '-'
                if piece.isupper():
                    gs.board.matrix[move.start_row][move.start_row+1] = 'R'
                else:
                    gs.board.matrix[move.start_row][move.start_row+1] = 'r' 
            elif move.end_col == move.start_col - 2: # Castling long
                gs.board.matrix[move.start_row][move.start_row-4] = '-'
                if piece.isupper():
                    gs.board.matrix[move.start_row][move.start_row-1] = 'R'
                else:
                    gs.board.matrix[move.start_row][move.start_row-1] = 'r'  
        return gs
               
    def change_player(self) -> None:
        """ Changes the flag that displays whose turn it is """
        self.flags["white_to_move"] = not self.flags["white_to_move"]

    def is_white_to_move(self) -> bool:
        """ Returns the flag that displays whose turn it is """
        return self.flags["white_to_move"]
    
    def is_check(self, move: 'Move') -> None:
        """ Calculates if the move results in a check """
        white_attacks = self.is_white_to_move() 
        gs = self.apply_move(move)
        for i in range(8):
            for j in range(8):
                if ((white_attacks) == (gs.board.matrix[i][j] == 'K')):
                    move.is_check = gs.is_square_under_attack(white_attacks, i, j)

    def is_checkmate(self, move: 'Move') -> None:
        """ Calculates if the move results in checkmate """
        if move.is_check == None:
            self.is_check(move)
        if not self.processed:
            self.generate_all_moves()
        move.is_checkmate = move.is_check and len(self.possible_moves) == 0
        
    def is_stalemate(self, move: 'Move') -> None:
        """ Calculates if the move results in stalemate """
        def is_stalemate_by_no_moves() -> None:
            if move.is_check == None:
                move.is_check()
            if not self.processed:
                self.generate_all_moves()
            move.is_checkmate = not move.is_check and len(self.possible_moves) == 0

        def is_stalemate_by_insufficient_material() -> bool:
            return (self.pieces == 2)

        def is_stalemate_by_threefold_repetition() -> bool:
            return False

        def is_stalemate_by_fifty_move_rule() -> bool:
            return (self.sm_counter == 50)
        
        move.is_stalemate = is_stalemate_by_no_moves() or is_stalemate_by_fifty_move_rule() or is_stalemate_by_insufficient_material() or is_stalemate_by_threefold_repetition()
  
    def is_empty_or_opponent_piece(self, row, col):
        """ Returns whether the square is empty or occupied by the opposing color or not"""
        if self.board.matrix[row][col] == '-':
            return True
        if self.is_white_to_move():
            return self.board.matrix[row][col].islower()
        return self.board.matrix[row][col].isupper()
    
    def is_valid_move(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        """ Returns whether the possible move is a valid one """
        return 0 <= end_row < 8 and 0 <= end_col < 8 and self.board.is_path_clear(start_row, start_col, end_row, end_col) and self.is_empty_or_opponent_piece(end_row, end_col)

    def is_square_under_attack(self, white_attacks, row, col) -> bool:
        """ Returns whether the square is under attack by the opposing color or not"""
        if white_attacks:
            for r in range(8):
                for c in range(8):
                    piece = self.board.matrix[r][c]
                    if piece.islower():
                        if self.is_valid_move(r, c, row, col):
                            return True
            return False
    
        else:
            for r in range(8):
                for c in range(8):
                    piece = self.board.matrix[r][c]
                    if piece.isupper():
                        if self.is_valid_move(r, c, row, col):
                            return True
            return False

    def is_capture(self, row, col, new_row, new_col) -> bool:
        if self.board.matrix[row][col] == '-' or self.board.matrix[new_row][new_col] == '-':
            return False
        return self.board.matrix[row][col].isupper() != self.board.matrix[new_row][new_col].isupper()

    def generate_pawn_moves(self, row: int, col: int) -> None:
        def setup(row: int, col: int, new_row, new_col):
            if self.is_valid_move(row, col, new_row, new_col):
                new_move = Move(row, col, new_row, new_col)
                self.possible_moves.append(new_move)

        if self.is_white_to_move():
            setup(row, col, row-1, col-1)
        else:
            setup(row, col, row-1, col+1)
        
        if self.is_white_to_move():
            setup(row, col, row-1, col-1)
        else:
            setup(row, col, row-1, col+1)
        
        if self.is_white_to_move():
            setup(row, col, row-1, col-2)
        else:
            setup(row, col, row-1, col+2)

    def generate_bishop_moves(self, row: int, col: int) -> None:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.move_builder(row, col, directions)

    def generate_rook_moves(self, row: int, col: int) -> None:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.move_builder(row, col, directions)

    def generate_queen_moves(self, row: int, col: int) -> None:
        self.generate_rook_moves(row, col)
        self.generate_bishop_moves(row, col)

    def generate_king_moves(self, row: int, col: int) -> None:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.move_builder(row, col, directions)
            
    def generate_knight_moves(self, row: int, col: int) -> None :
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self.move_builder(row, col, directions)

    def move_builder(self, row: int, col: int, directions: List[int]):
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_move(row, col, new_row, new_col):
                new_move = Move(row, col, new_row, new_col)
                self.possible_moves.append(new_move)

    def generate_all_moves(self) -> None:
        for i in range(8):
            for j in range(8):
                match self.board.matrix[i][j].upper():
                    case "P":
                        self.generate_pawn_moves(i, j)
                    case "Q":
                        self.generate_queen_moves(i, j)
                    case "N":
                        self.generate_knight_moves(i, j)
                    case "B":
                        self.generate_bishop_moves(i, j)
                    case "R":
                        self.generate_rook_moves(i, j)
                    case "K":
                        self.generate_king_moves(i, j)
                    case _:
                        pass
