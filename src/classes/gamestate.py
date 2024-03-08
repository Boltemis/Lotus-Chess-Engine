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
        copy = Gamestate(board, self.flags)
        copy.change_player()
        return copy

    def change_player(self) -> None:
        self.flags["white_to_move"] = not self.flags["white_to_move"]

    def is_white_to_move(self) -> bool:
        return self.flags["white_to_move"]

    def is_check(self) -> bool:
        pass

    def is_checkmate(self) -> bool:
        return False

    def is_stalemate(self) -> bool:
        return False

    def is_stalemate_by_insufficient_material(self) -> bool:
        pass

    def is_stalemate_by_threefold_repetition(self) -> bool:
        pass

    def is_stalemate_by_fifty_move_rule(self) -> bool:
        pass

    def is_square_under_attack(self, square) -> bool:
        pass