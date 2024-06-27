class Board:
    def __init__(self, matrix):
        self.matrix = matrix

    def is_path_clear(self, start_row, start_col, end_row, end_col):
        """ Calculates if the path from the start square to the end square is empty """
        if self.matrix[start_row][start_col].lower() == 'n':
            return True
        if start_row == end_row:
            direction = 1 if end_col > start_col else -1
            for col in range(start_col + direction, end_col, direction):
                if self.matrix[start_row][col] != '-':
                    return False
        elif start_col == end_col:
            direction = 1 if end_row > start_row else -1
            for row in range(start_row + direction, end_row, direction):
                if self.matrix[row][start_col] != '-':
                    return False
        else:
            row_direction = 1 if end_row > start_row else -1
            col_direction = 1 if end_col > start_col else -1
            row, col = start_row + row_direction, start_col + col_direction
            while row != end_row and col != end_col:
                if self.matrix[row][col] != '-':
                    return False
                row += row_direction
                col += col_direction
        return True

    def matrix_copy(self):
        return [r[:] for r in self.matrix]