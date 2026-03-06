"""
Thuật toán A* (A-star) cho Word Search.
"""
from dataclasses import dataclass
import heapq
import time
import tracemalloc


@dataclass(order=True)
class _AStarNode:
    """Node nội bộ cho A*: f = g + h."""
    f_cost: int
    g_cost: int
    row: int
    col: int
    index: int
    direction_idx: int


class WordSearchHeuristics:
    """
    Solver Word Search dùng A* + heuristic pruning.

    Interface tương thích với GUI:
    - directions, direction_names
    - find_word(word, verbose=False)
    - solve(verbose=False, step_by_step=False)
    - visualize_result()
    Helper functions:
    - _sort_words_by_priority(), _get_promising_directions(), _check_word_fits()
    """

    def __init__(self, grid):
        self.grid = grid
        self.size = grid.size
        self.found_words = {}
        self.nodes_explored = 0

        self.directions = [
            (0, 1),    # ngang phải
            (1, 0),    # dọc xuống
            (1, 1),    # chéo phải xuống
            (1, -1),   # chéo trái xuống
            (0, -1),   # ngang trái
            (-1, 0),   # dọc lên
            (-1, -1),  # chéo trái lên
            (-1, 1),   # chéo phải lên
        ]
        self.direction_names = [
            "ngang phải",
            "dọc xuống",
            "chéo phải xuống",
            "chéo trái xuống",
            "ngang trái",
            "dọc lên",
            "chéo trái lên",
            "chéo phải lên",
        ]

        self.char_positions = self._build_char_positions()
        self.char_frequency = {ch: len(pos_list) for ch, pos_list in self.char_positions.items()}

    def _build_char_positions(self):
        """Lập chỉ mục vị trí ký tự: char -> [(row, col), ...]."""
        positions = {}
        for r in range(self.size):
            for c in range(self.size):
                ch = self.grid.get_cell(r, c)
                positions.setdefault(ch, []).append((r, c))
        return positions

        

    def _remaining_cost(self, word_len, index):
        """Heuristic h(n): số ký tự còn lại cần khớp."""
        return word_len - index

    def _sort_words_by_priority(self, words):
        """
        Sắp từ theo độ ưu tiên:
        - ký tự đầu hiếm hơn => ưu tiên hơn
        - từ dài hơn => ưu tiên hơn
        """
        def priority(w):
            wu = w.upper()
            first_freq = self.char_frequency.get(wu[0], 10**9)
            return (first_freq, -len(wu), wu)

        return sorted(words, key=priority)

    def _check_word_fits(self, word, row, col, direction):
        """Kiểm tra nhanh từ có vượt biên nếu đi theo direction không."""
        dr, dc = direction
        end_row = row + (len(word) - 1) * dr
        end_col = col + (len(word) - 1) * dc
        return 0 <= end_row < self.size and 0 <= end_col < self.size

    def _get_promising_directions(self, word, row, col):
        """
        Lọc hướng triển vọng:
        - phải fit biên
        - nếu từ dài >= 2 thì ký tự thứ 2 phải khớp
        """
        word = word.upper()
        if len(word) <= 1:
            return list(range(len(self.directions)))

        second_char = word[1]
        promising = []

        for dir_idx, (dr, dc) in enumerate(self.directions):
            if not self._check_word_fits(word, row, col, (dr, dc)):
                continue
            nr, nc = row + dr, col + dc
            if self.grid.get_cell(nr, nc) == second_char:
                promising.append(dir_idx)

        return promising

    def _a_star_from_start(self, word, start_row, start_col, direction_candidates):
        """
        Chạy A* từ một ô bắt đầu, duy trì 1 hướng cố định cho mỗi nhánh.
        State: (row, col, index, direction_idx)
        """
        word = word.upper()
        goal_index = len(word)

        open_heap = []
        came_from = {}
        best_g = {}

        for dir_idx in direction_candidates:
            start_node = _AStarNode(
                f_cost=self._remaining_cost(len(word), 1),
                g_cost=1,
                row=start_row,
                col=start_col,
                index=1,
                direction_idx=dir_idx,
            )
            state = (start_row, start_col, 1, dir_idx)
            best_g[state] = 1
            came_from[state] = None
            heapq.heappush(open_heap, start_node)

        while open_heap:
            current = heapq.heappop(open_heap)
            self.nodes_explored += 1

            if current.index == goal_index:
                path = []
                state = (current.row, current.col, current.index, current.direction_idx)
                while state is not None:
                    r, c, _, _ = state
                    path.append((r, c))
                    state = came_from[state]
                path.reverse()
                return path, current.direction_idx

            dr, dc = self.directions[current.direction_idx]
            nr = current.row + dr
            nc = current.col + dc
            next_index = current.index + 1

            if not (0 <= nr < self.size and 0 <= nc < self.size):
                continue
            if word[current.index] != self.grid.get_cell(nr, nc):
                continue

            next_state = (nr, nc, next_index, current.direction_idx)
            tentative_g = current.g_cost + 1
            old_g = best_g.get(next_state)
            if old_g is not None and tentative_g >= old_g:
                continue

            best_g[next_state] = tentative_g
            came_from[next_state] = (current.row, current.col, current.index, current.direction_idx)
            h = self._remaining_cost(len(word), next_index)
            heapq.heappush(
                open_heap,
                _AStarNode(
                    f_cost=tentative_g + h,
                    g_cost=tentative_g,
                    row=nr,
                    col=nc,
                    index=next_index,
                    direction_idx=current.direction_idx,
                ),
            )

        return None, None

    def find_word(self, word, verbose=False):
        """Tìm 1 từ bằng A* + pruning."""
        word = word.upper()
        if not word:
            return None

        first_char = word[0]
        start_positions = self.char_positions.get(first_char, [])
        if not start_positions:
            return None

        for row, col in start_positions:
            direction_candidates = self._get_promising_directions(word, row, col)
            if not direction_candidates:
                continue

            path, direction_idx = self._a_star_from_start(word, row, col, direction_candidates)
            if path:
                return {
                    "word": word,
                    "start": path[0],
                    "end": path[-1],
                    "direction": self.direction_names[direction_idx],
                    "path": path,
                }
        return None

    def solve(self, verbose=False, step_by_step=False):
        """Giải toàn bộ puzzle với A*."""
        self.found_words = {}
        self.nodes_explored = 0

        words_to_search = self._sort_words_by_priority(self.grid.words)

        tracemalloc.start()
        start_time = time.time()

        for word in words_to_search:
            if step_by_step:
                self.grid.display()
            result = self.find_word(word, verbose=verbose or step_by_step)
            if result:
                self.found_words[word.upper()] = result
                if step_by_step:
                    self.grid.display(highlight_positions=result["path"])
                    input("   Nhấn Enter để tiếp tục...")

        elapsed_time = time.time() - start_time
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_used = peak / 1024 / 1024

        return {
            "found_words": self.found_words,
            "total_words": len(self.grid.words),
            "found_count": len(self.found_words),
            "time": elapsed_time,
            "memory": memory_used,
            "nodes_explored": self.nodes_explored,
        }

    def visualize_result(self):
        """Hiển thị lưới với tất cả từ đã tìm thấy."""
        all_positions = set()
        for info in self.found_words.values():
            all_positions.update(info["path"])

        self.grid.display(highlight_positions=all_positions)
