import unittest

from classes.gamestate import *
from utils import *

START_FLAGS: dict[str: bool] = {
    "white_king_moved": False, 
    "left_white_rook_moved": False, 
    "right_white_rook_moved": False, 
    "black_king_moved": False,
    "left_black_rook_moved": False, 
    "right_black_rook_moved": False, 
    "white_to_move": True
    }

START_BOARD: List[str] = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['-', '-', '-', '-', '-', '-', '-', '-'], 
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

class TestMoveGeneration(unittest.TestCase):
    def test_copy(self):
        gs = Gamestate(Board(START_BOARD), START_FLAGS, 0, 32, 0)
        new_gs = gs.copy()
        new_gs.board.matrix[4][2] = 'R'
        self.assertNotEqual(gs.board.matrix[4][2], new_gs.board.matrix[4][2])

    def test_change_player(self):
        gs = Gamestate(Board(START_BOARD), START_FLAGS, 0, 32, 0)
        self.assertTrue(gs.is_white_to_move())
        gs.change_player()
        self.assertFalse(gs.is_white_to_move())
        gs.change_player()
        self.assertTrue(gs.is_white_to_move())

    def test_is_capture(self):
        gs =  Gamestate(Board(START_BOARD), START_FLAGS, 0, 32, 0)
        self.assertTrue(gs.is_capture(0, 0, 7, 7))
        self.assertFalse(gs.is_capture(3, 0, 7, 7))
        self.assertFalse(gs.is_capture(0, 0, 3, 7))
        self.assertFalse(gs.is_capture(3, 0, 3, 7))
        self.assertFalse(gs.is_capture(0, 0, 0, 1))
        self.assertFalse(gs.is_capture(7, 7, 7, 7))

    def test_is_empty_or_opponent_piece(self):
        gs = Gamestate(Board(START_BOARD), START_FLAGS, 0, 32, 0)
        self.assertTrue(gs.is_empty_or_opponent_piece(4, 4))
        self.assertTrue(gs.is_empty_or_opponent_piece(0, 0))
        self.assertFalse(gs.is_empty_or_opponent_piece(7, 7))
        gs.change_player()
        self.assertTrue(gs.is_empty_or_opponent_piece(4, 4))
        self.assertFalse(gs.is_empty_or_opponent_piece(0, 0))
        self.assertTrue(gs.is_empty_or_opponent_piece(7, 7))

    def test_is_path_clear(self):
        board = Board(START_BOARD)
        self.assertFalse(board.is_path_clear(7, 0, 7, 7))
        self.assertTrue(board.is_path_clear(1, 4, 6, 4))
        self.assertFalse(board.is_path_clear(1, 4, 7, 4))
        self.assertFalse(board.is_path_clear(0, 0, 3, 3))
        self.assertTrue(board.is_path_clear(4, 4, 4, 4))

    def test_is_square_under_attack(self):
        pass

    def test_is_check(self):
        pass
    


if __name__ == '__main__':
    unittest.main()