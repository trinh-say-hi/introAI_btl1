import os
import sys


CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from grid import Grid
from word_search_dfs import WordSearchDFS
from word_search_heuristics import WordSearchHeuristics


def _load_easy_grid():
    grid = Grid()
    filepath = os.path.join(PROJECT_ROOT, "input", "easy.txt")
    grid.load_from_file(filepath)
    return grid


def test_load_easy_grid():
    grid = _load_easy_grid()
    assert grid.size == 8
    assert len(grid.words) == 10
    assert grid.get_cell(0, 0) == "C"


def test_dfs_find_word_cat():
    grid = _load_easy_grid()
    solver = WordSearchDFS(grid)
    result = solver.find_word("CAT")
    assert result is not None
    assert result["word"] == "CAT"
    assert len(result["path"]) == 3


def test_a_star_find_word_cat():
    grid = _load_easy_grid()
    solver = WordSearchHeuristics(grid)
    result = solver.find_word("CAT")
    assert result is not None
    assert result["word"] == "CAT"
    assert len(result["path"]) == 3
