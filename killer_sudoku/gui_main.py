import pygame
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.Astar.main import read_file
from src.Astar.solver import AStarSolver
from src.DFS.dfs_logic import DFSSudokuSolver
from src.visualizer import Visualizer

def get_solver_instance(algo_name, board, cages):
    if algo_name == "A* Search":
        return AStarSolver(board, cages)
    else:
        dfs_cages = [{"sum": c.target_sum, "cells": c.cells} for c in cages]
        return DFSSudokuSolver(board, dfs_cages, os.path.join(BASE_DIR, "output", "gui_dfs_temp.txt"))

if __name__ == "__main__":
    pygame.init()

    input_folder = os.path.join(BASE_DIR, "input")
    input_file = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    algorithms = ["DFS Logic", "A* Search"]

    selected_file = "easy.txt"
    selected_algo = "DFS Logic"

    board, cages, size = read_file(os.path.join(input_folder, selected_file))
    vis = Visualizer(size=size, window_width=600)
    solver = get_solver_instance(selected_algo, board, cages)

    solve_gen = None
    running = True
    solving = False
    is_paused = False
    speed = 250
    current_board = board
    last_move = None

    while running:
        if current_board is not None:
            vis.draw_grid(current_board, last_move)
            vis.draw_cages(cages)
        algo_rects, file_rects = vis.draw_sidebar(algorithms, selected_algo, input_file, selected_file)
        vis.draw_info(solver.nodes_expanded, speed, is_paused)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # Click to choose algorithm
                for algo, rect in algo_rects.items():
                    if rect.collidepoint(pos):
                        selected_algo = algo
                        solving = False
                        solve_gen = None

                        current_board = [row[:] for row in board]
                        last_move = None
                        vis = Visualizer(size=size)
                        solver = get_solver_instance(selected_algo, current_board, cages)

                # Click to choose test
                for f_name, rect in file_rects.items():
                    if rect.collidepoint(pos):
                        selected_file = f_name
                        solving = False
                        solve_gen = None
                        
                        board, cages, size = read_file(os.path.join(input_folder, f_name))
                        current_board = [row[:] for row in board]
                        last_move = None
                        vis = Visualizer(size=size)
                        solver = get_solver_instance(selected_algo, current_board, cages)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solving = True
                    if not solve_gen:
                        solve_gen = solver.solve_visualize()
                if event.key == pygame.K_p: #press P to pause
                    is_paused = not is_paused
                if event.key == pygame.K_UP:
                    speed = max(10, speed - 10)
                if event.key == pygame.K_DOWN:
                    speed += 10
                if event.key == pygame.K_ESCAPE:
                    running = False

        if solving and not is_paused and solve_gen:
            try:
                step_res = next(solve_gen)
                board_at_step, finished, highlight = step_res

                if current_board is not None:
                    current_board = board_at_step
                    last_move = highlight

                    vis.draw_grid(current_board, highlight)
                    vis.draw_cages(cages)
                    pygame.display.flip()
                    pygame.time.delay(int(speed * 0.7))

                    vis.draw_grid(current_board)
                    vis.draw_cages(cages)
                    pygame.display.flip()
                    pygame.time.delay(int(speed * 0.3))
                else:
                    print("Không tìm thấy lời giải!")
                    solving = False

                if finished:
                    solving = False
            except StopIteration:
                solving = False
        
        pygame.display.flip()
    pygame.quit()