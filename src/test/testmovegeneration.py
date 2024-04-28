import unittest
import sys
sys.path.append('../')

from src.classes.gamestate import *

class TestMoveGeneration(unittest.TestCase):
    def test_pawn(self):
        board: List[List][str] = [
                                ['-', '-', '-', '-', '-', '-', '-', '-'], 
                                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                                ['p', 'P', '-', 'P', '-', '-', 'p', '-'], 
                                ['-', '-', '-', '-', 'p', '-', '-', '-'], 
                                ['-', '-', '-', '-', 'P', '-', '-', '-'], 
                                ['P', 'p', '-', '-', '-', '-', 'P', '-'], 
                                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                                ['-', '-', '-', '-', '-', '-', '-', '-']
                                ]
        pawn_gs = Gamestate(board)
        pawn_moves = pawn_gs.generate_all_moves(True)
        self.assertEqual(len(pawn_moves), 17)            

    def test_bishop(self):
        board: List[List][str] = [
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['b', '-', '-', '-', '-', '-', 'b', '-'], 
                        ['-', '-', '-', '-', 'b', '-', '-', '-'], 
                        ['-', 'b', '-', 'B', '-', '-', '-', '-'], 
                        ['-', '-', 'B', 'B', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-']
                        ]
        bishop_gs = Gamestate(board)
        bishop_moves = bishop_gs.generate_all_moves(True)
        self.assertEqual(len(bishop_moves), 22) 

    def test_rook(self):
        board: List[List][str] = [
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', 'r', '-', 'R', '-', '-', '-', 'R'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ]
        rook_gs = Gamestate(board)
        rook_moves = rook_gs.generate_all_moves(True)
        self.assertEqual(len(rook_moves), 22) 

    def test_queen(self):
        board: List[List][str] = [
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['q', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', 'q', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', 'r', '-', 'Q', '-', '-', '-', 'Q'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ]
        rook_gs = Gamestate(board)
        rook_moves = rook_gs.generate_all_moves(True)
        self.assertEqual(len(rook_moves), 38) 
    
    def test_king(self):
        board: List[List][str] = [
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'], 
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', 'r'], 
                        ['-', '-', '-', '-', 'K', '-', '-', 'R'],
                        ]
        king_gs = Gamestate(board)
        king_gs.flags["left_white_rook_moved"] = True
        king_moves = king_gs.generate_all_moves(True)
        self.assertEqual(len(king_moves), 6) 

if __name__ == '__main__':
    unittest.main()