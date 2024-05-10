class Move:
    def __init__(self, start_col, start_row, end_col, end_row):
        self.start_col = start_col
        self.start_row = start_row
        self.end_col = end_col
        self.end_row = end_row
        self.is_check = None
        self.is_checkmate = None
        self.is_stalemate = None
        
