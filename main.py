import time
import tracemalloc
import os


class KillerSudokuBoard:
    def __init__(self, board, cages):
        if len(board) != 9 or any(len(row) != 9 for row in board):
            raise ValueError("Invalid Sudoku board size")
        self.board = board
        self.cages = cages
        self.final_steps = []  

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col
        return None

    def get_cage(self, row, col):
        for cage in self.cages:
            if (row, col) in cage["cells"]:
                return cage
        return None
    
    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
            
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
                
        cage = self.get_cage(row, col)
        if cage:
            current_sum = num
            used_numbers = [num]

            for (r, c) in cage["cells"]:
                if self.board[r][c] != 0:
                    current_sum += self.board[r][c]
                    used_numbers.append(self.board[r][c])

            if len(used_numbers) != len(set(used_numbers)):
                return False
            
            if current_sum > cage["sum"]:
                return False
            
            if all(self.board[r][c] != 0 for (r, c) in cage["cells"]):
                if current_sum != cage["sum"]:
                    return False
                
        return True

    def print_board(self, file=None):
        output = []
        for row in self.board:
            output.append(" ".join(str(num) for num in row))
        board_str = "\n".join(output) + "\n"

        if file:
            file.write(board_str + "\n")
        else:
            print(board_str)


class DFSSudokuSolver:
    def __init__(self, board, cages, output_file):
        self.board = KillerSudokuBoard(board, cages)
        self.expanded_states = 0
        self.visited_states = 0
        self.output_file = output_file

    def solve(self):
        with open(self.output_file, "w", encoding="utf-8") as f:  
            f.write("=== Start solving Sudoku using DFS ===\n\n")

            start_time = time.time()
            tracemalloc.start()

            if self.dfs():
                end_time = time.time()
                current_memory, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                for step_num, (row, col, num) in enumerate(self.board.final_steps):
                    f.write(f"Step {step_num}: Placed {num} in cell ({row}, {col})\n")
                    self.board.print_board(f) 

                f.write("\nSolution found!\n")
                f.write(f"Total expanded states: {self.expanded_states}\n")
                f.write(f"Total visited states: {self.visited_states}\n")
                f.write(f"Execution time: {end_time - start_time:.6f} seconds\n")
                f.write(f"Memory usage: {current_memory} Bytes\n")
                f.write("---------------------------\n")

                self.board.print_board(f)
            else:
                f.write("\nNo solution exists.\n")

    def dfs(self):
        empty = self.board.find_empty()
        if not empty:
            return True

        row, col = empty

        for num in range(1, 10):
            if self.board.is_valid(row, col, num):
                self.board.board[row][col] = num
                self.expanded_states += 1
                self.visited_states += 1

                if self.dfs():
                    self.board.final_steps.append((row, col, num)) 
                    return True

                self.board.board[row][col] = 0

        return False


def read_sudoku_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    board = []
    for i in range(9):
        board.append(list(map(int, lines[i].split())))

    cage_count = int(lines[9].strip())

    cages = []
    for i in range(10, 10 + cage_count):
        parts = lines[i].strip().split()
        cage_sum = int(parts[0])

        cells = []
        for cell in parts[1:]:
            r, c = map(int, cell.split(","))
            cells.append((r, c))

        cages.append({
            "cells": cells,
            "sum": cage_sum
        })

    return board, cages


def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    input_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    if not input_files:
        print("No input files found in the 'input/' directory.")
        return

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, input_file.replace("input", "output"))

        print(f"Processing: {input_file} → {output_path}")

        board, cages = read_sudoku_from_file(input_path)

        solver = DFSSudokuSolver(board, cages, output_path)
        solver.solve()

    print("\nAll files have been processed.")
    print(f"Results are saved in the '{output_dir}' directory.")


if __name__ == "__main__":
    main()
    
