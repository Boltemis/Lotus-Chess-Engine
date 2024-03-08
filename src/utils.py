from typing import List


def board_to_fen(board) -> str:
    """ converts a board state to FEN """
    fen = ''
    for row in board:
        counter = 0
        for square in row:
            if square == '-':
                counter += 1
            else:
                if counter:
                    fen += str(counter)
                    counter = 0
                fen += square   
        if counter:
            fen += str(counter)
        fen += '/'
    return fen[:-1]

def fen_to_board(fen) -> List[List[str]]:
    """ converts a FEN to a board state """
    board = [[] for _ in range(8)]
    row = 0
    for char in fen:
        if char.isdigit() and 1 <= int(char) <= 8:
            for _ in range(int(char)):
                board[row].append('-')
        elif char == '/':
            row += 1
        else:
            board[row].append(char)
    return board    