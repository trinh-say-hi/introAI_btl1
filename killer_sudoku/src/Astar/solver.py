import heapq
import time
import tracemalloc

try:
    from .board import Cage, Board
    from .heuristic import Heuristic
    from .utils import KillerSudokuUtils
except ImportError:
    from board import Cage, Board
    from heuristic import Heuristic
    from utils import KillerSudokuUtils

class AStarSolver:
    def __init__(self, initial_board, cages):
        self.board = initial_board
        self.cages = cages

        self.board_obj = Board(self.board, self.cages)

        self.nodes_expanded = 0
        self.memory_usage = 0

    def solve(self):
        """ Terminal/Benchmark"""
        gen = self.solve_visualize()
        try:
            while True:
                next(gen)
        except StopIteration as e:
            return e.value
        
    def solve_visualize(self):
        """ GUI """
        n = len(self.board)

        start_time = time.time()
        tracemalloc.start()
        pq = []
        visited = set()

        initial_h = Heuristic.calculate(self.board_obj.board)
        heapq.heappush(pq, (initial_h, 0, self.board, None))
        visited.add(tuple(map(tuple, self.board)))

        while pq:
            f, g, current_board, last_move = heapq.heappop(pq)
            self.nodes_expanded += 1
            
            yield current_board, False, last_move

            empty = self.board_obj.find_empty(current_board)
            if not empty:
                self.memory_usage, _ = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                end_time = time.time()
                
                yield current_board, True, last_move              
                return current_board, end_time - start_time, self.nodes_expanded, self.memory_usage
            
            row, col = empty
            for num in range(1, n + 1):
                if KillerSudokuUtils.is_valid(current_board, row, col, num, self.board_obj):
                    new_board = [row[:] for row in current_board]
                    new_board[row][col] = num
                    board_tuple = tuple(map(tuple, new_board))

                    if board_tuple not in visited:
                        visited.add(board_tuple)

                        new_g = g + 1
                        new_h = Heuristic.calculate(new_board)
                        heapq.heappush(pq, (new_g + new_h, new_g, new_board, (row, col)))

        tracemalloc.stop()
        yield None, True, None

        return None, None, None, None