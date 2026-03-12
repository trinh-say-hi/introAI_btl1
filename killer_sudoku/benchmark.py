import os
import sys
import time
import tracemalloc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.Astar.main import read_file
from src.Astar.solver import AStarSolver
from src.DFS.dfs_logic import DFSSudokuSolver

INPUT_FOLDER = os.path.join(BASE_DIR, "input")

def run():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Lỗi: Không tìm thấy thư mục đầu vào tại: {INPUT_FOLDER}")
        return

    input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")]

    if not input_files:
        print(f"Không tìm thấy file nào trong {INPUT_FOLDER}")
        return
    
    header = f"{f"{'File':<15} | {'Algo':<8} | {'Status':<10} | {'Nodes':<9} | {'Time (s)':<10} | {'Memory (KB)':<10}"}"
    print("\n" + "="*80)
    print("KILLER SUDOKU BENCHMARK: A* vs DFS")
    print("="*80)
    print(header)
    print("-" * 80)

    for file_name in input_files:
        path = os.path.join(INPUT_FOLDER, file_name)
        
        try:
            board, cages, size = read_file(path)

            """A*"""
            astar_solver = AStarSolver([row[:] for row in board], cages)
            astar_result, astar_duration, astar_nodes, astar_memory = astar_solver.solve()

            atsar_status = "Solved" if astar_result else "Failed"

            print(f"{file_name:<15} | {'A*':<8} | {atsar_status:<10} |{astar_nodes:<10} | {astar_duration:<10.4f} | {astar_memory/1024:<10.2f}")

            """DFS"""
            dfs_cages = [{"sum": c.target_sum, "cells": c.cells} for c in cages]

            try:
                dfs_solver = DFSSudokuSolver([row[:] for row in board], dfs_cages, os.devnull)

                tracemalloc.start()
                start_t = time.time()
                dfs_success = dfs_solver.dfs()
                dfs_duration = time.time() - start_t
                dfs_memory, _ = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                dfs_status = "Solved" if dfs_success else "Failed"
                
                print(f"{'':<15} | {'DFS':<8} | {dfs_status:<10} |{dfs_solver.expanded_states:<10} | {dfs_duration:<10.4f} | {dfs_memory/1024:<10.2f}")
            except ValueError:
                print(f"{'':<15} | {'DFS':<8} | {'Skipped':<10} |{'-':<10} | {'-':<10} | {'-':<10} (9x9 only)")
            
            print("-" * 80)
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_name}: {e}")

if __name__ == "__main__":
    run()