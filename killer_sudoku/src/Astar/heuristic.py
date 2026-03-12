class Heuristic:
    @staticmethod
    def calculate(board):
        return sum(row.count(0) for row in board)