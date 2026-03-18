import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'UI'))
sys.path.append(os.path.dirname(__file__))

from UI.grid import Grid
from Algorithm.DFS import WordSearchDFS
from Algorithm.A_star import WordSearchHeuristics
from Algorithm.Greedy_BFF import WordSearchGreedyBestFirst

SOLVERS = [
    ("DFS", WordSearchDFS),
    ("A_STAR", WordSearchHeuristics),
    ("GREEDY_BFF", WordSearchGreedyBestFirst),
]

TEST_CASES = [
    ('Easy', os.path.join(os.path.dirname(__file__), 'input', 'easy.txt')),
    ('Medium', os.path.join(os.path.dirname(__file__), 'input', 'medium.txt')),
    ('Hard', os.path.join(os.path.dirname(__file__), 'input', 'hard.txt'))
]

def run_benchmark():
    print("BẢNG SO SÁNH KẾT QUẢ")
    print(f"{'Thuật toán':<15} | {'Test Case':<10} | {'Thời gian (s)':<15} | {'Bộ nhớ (MB)':<15} | {'Nodes':<10} | {'Tìm thấy':<10}")
    print("-" * 85)

    for solver_name, solver_class in SOLVERS:
        for test_name, filepath in TEST_CASES:
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}")
                continue
            
            grid = Grid()
            grid.load_from_file(filepath)
            
            solver = solver_class(grid)
            
            # Run solve
            result = solver.solve(verbose=False, step_by_step=False)
            
            time_s = result.get('time', 0)
            mem_mb = result.get('memory', 0)
            nodes = result.get('nodes_explored', 0)
            found = f"{result.get('found_count', 0)}/{result.get('total_words', 0)}"
            
            print(f"{solver_name:<15} | {test_name:<10} | {time_s:<15.6f} | {mem_mb:<15.6f} | {nodes:<10} | {found:<10}")

if __name__ == '__main__':
    run_benchmark()
