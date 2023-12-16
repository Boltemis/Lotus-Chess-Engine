#converts a 64 bit binary number to a decimal
def bits_to_number(bits):
    if len(bits) > 64:
        return -1

    number = 0

    for i in range(0, len(bits)):
        if bits[-(i+1)] == '1':
            number += 2**i
        elif bits[-(i+1)] != '0':
            return -1

    return number

#converts a decimal to a 64 bit binary number
def number_to_bits(number):
    if number > 18_446_744_073_709_551_615:
        return -1

    bits = ''

    for i in range(63, -1, -1):
        if number - (2**i) >= 0:
            bits += '1'
            number -= 2**i
        else:
            bits += '0'
        if number == 0:
            while (len(bits) != 64):
                bits += '0'
                
            return bits

    return -1

#converts a board state to FEN
def board_to_fen(board):
    fen = ''

    for i in range(len(board)):
        counter = 0
        for j in range(len(board[i])):
            if board[i][j] == '-':
                counter += 1
            else:
                if counter != 0:
                    fen += str(counter)
                    counter = 0
                fen += board[i][j]
        if counter != 0:
            fen += str(counter)
        fen += '/'


    return fen

#converts a FEN to a board state
def fen_to_board(fen):
    board = [[], [], [], [], [], [], [], []]
    row = 0
    for char in fen:
        if char.isdigit() and 1 <= int(char) <= 8:
            for i in range(int(char)):
                board[row].append('-')
        elif char == '/':
            row += 1
        else:
            board[row].append(char)

    return board

#converts a board state to an array of 12 tuples (identificator, bitnumber)
def boardstate_to_bits(board):
    arr = [('white_pawn_bits', 'P'), ('white_rook_bits', 'R'), ('white_knight_bits', 'N'),
       ('white_bishop_bits', 'B'), ('white_queen_bits', 'Q'), ('white_king_bits', 'K'),
       ('black_pawn_bits', 'p'), ('black_rook_bits', 'r'), ('black_knight_bits', 'n'),
       ('black_bishop_bits', 'b'), ('black_queen_bits', 'q'), ('black_king_bits', 'k')]

    bits = []

    for _, piece_type in arr:
        bit_string = ''
        for row in board:
            for char in row:
                bit_string += '1' if char == piece_type else '0'
        bits.append((bit_string, piece_type))

    return bits