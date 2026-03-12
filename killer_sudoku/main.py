import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.Astar.main import read_file, save_to_file
from src.Astar.solver import AStarSolver
from src.DFS.dfs_logic import DFSSudokuSolver

INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

def run():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if not os.path.exists(INPUT_FOLDER):
        print(f"Lỗi: Không tìm thấy thư mục đầu vào tại: {INPUT_FOLDER}")
        return

    input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")]

    if not input_files:
        print(f"Không tìm thấy file nào trong {INPUT_FOLDER}")
        return
    
    algorithms = ["A*", "DFS"]
    
    for file_name in input_files:
        input_path = os.path.join(INPUT_FOLDER, file_name)
        print(f"\n{'='*50}")
        print(f"ĐANG XỬ LÝ FILE: {file_name}")
        print(f"\n{'='*50}")

        for algo_name in algorithms:
            safe_algo_name = algo_name.replace("*", "Star")
            output_path = os.path.join(OUTPUT_FOLDER, f"{safe_algo_name}_{file_name}")

            print(f"\n>>> Giải thuật: {algo_name}")

            board, cages, size = read_file(input_path)
            if algo_name == "A*":
                solver = AStarSolver(board, cages)
                result_board, duration, nodes, memory = solver.solve()

                if result_board:
                    print(f"    [A*] Thành công! Time: {duration:.4f}s | Nodes: {nodes}")
                    save_to_file(output_path, result_board, duration, nodes, memory)
                else:
                    print(f"    [A*] Không tìm thấy lời giải.")
            elif algo_name == "DFS":
                dfs_cages = [{"sum": c.target_sum, "cells": c.cells} for c in cages]
                solver = DFSSudokuSolver(board, dfs_cages, output_path)
                solver.solve()
                print(f"    [DFS] Hoàn tất! Kết quả chi tiết đã được lưu vào: {output_path}")

if __name__ == "__main__":
    run()