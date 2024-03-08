from typing import List
from utils import *

class Gamestate:
    def __init__(self):
        self.board: List[List][str] = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                      ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        
        self.pieces_left: int = 32
    
        # should default to false
        self.ep_flag_array: List[bool] = [[False] * 8 for _ in range(2)]
        # once true should remain true
        self.wking_moved: bool = False
        self.wlrook_moved: bool = False
        self.wrrook_moved: bool = False
        self.bking_moved: bool = False
        self.blrook_moved: bool = False
        self.brrook_moved: bool = False
        # should swap every creation
        self.white_to_move: bool = True

        self.fifty_move_counter: int = 0
        self.threefold_repetition_counter: int = 0
    
    def is_check() -> bool:
        pass

    def is_checkmate() -> bool:
        pass

    def is_stalemate() -> bool:
        pass

    def is_stalemate_by_insufficient_material() -> bool:
        pass

    def is_stalemate_by_threefold_repetition() -> bool:
        pass

    def is_stalemate_by_fifty_move_rule() -> bool:
        pass

    def is_square_under_attack(square) -> bool:
        pass