try:
    from .utils import KillerSudokuUtils
except ImportError:
    from utils import KillerSudokuUtils

class Cage:
    def __init__(self, target_sum, cells):
        self.target_sum = target_sum
        self.cells = cells

class Board:
    def __init__(self, board, cages):
        self.board = board
        self.n = len(board)
        self.cages = cages
        self.cage_map = {}

        for cage in self.cages:
            for row, col in cage.cells:
                self.cage_map[(row, col)] = cage

    def find_empty(self, board):
        best_cell = None
        min_choices = float('inf')

        for row in range(self.n):
            for col in range(self.n):
                if board[row][col] == 0:
                    choices = 0
                    
                    for num in range(1, self.n + 1):
                        if KillerSudokuUtils.is_valid(board, row, col, num, self):
                            choices += 1
                    
                    if choices < min_choices:
                        min_choices = choices
                        best_cell = (row, col)
                    
                    if min_choices == 1:
                        return best_cell

        return best_cell