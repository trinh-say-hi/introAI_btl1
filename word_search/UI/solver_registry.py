"""
Registry thuật toán cho Word Search GUI.

Format chung để thêm solver mới:
1) Class constructor nhận `grid`
2) Có `directions` và `direction_names`
3) (Tùy chọn) hỗ trợ các hook:
   - `_sort_words_by_priority(words)`
   - `char_positions`
   - `_get_promising_directions(word, row, col)`
   - `_check_word_fits(word, row, col, direction)`
"""
from Algorithm.DFS import WordSearchDFS
from Algorithm.A_star import WordSearchHeuristics
from Algorithm.Greedy_BFF import WordSearchGreedyBestFirst


SOLVER_REGISTRY = [
    ("DFS", WordSearchDFS),
    ("A_STAR", WordSearchHeuristics),
    ("GREEDY_BFF", WordSearchGreedyBestFirst),
]


def get_solver_options():
    """Trả về danh sách tuple (display_name, solver_class)."""
    return list(SOLVER_REGISTRY)
