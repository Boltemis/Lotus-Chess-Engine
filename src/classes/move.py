class Move:
    def __init__(self, start_row, start_col, end_row, end_col):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.is_check = None
        self.is_checkmate = None
        self.is_stalemate = None
    
    def print_move(self):
        print(self.start_col, self.start_row, self.end_col, self.end_row)

    def equals(self, move: 'Move'):
        return (self.start_col == move.start_col) and (self.start_row == move.start_row) and (self.end_col == move.end_col) and (self.end_row == move.end_row)
        
