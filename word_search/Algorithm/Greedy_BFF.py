"""
Greedy Best-First Search cho Word Search.
"""
import heapq
import time
import tracemalloc


class WordSearchGreedyBestFirst:
    def __init__(self, grid):
        self.grid = grid
        self.size = grid.size
        self.found_words = {}
        self.nodes_explored = 0

        # 8 hướng chuẩn
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
        positions = {}
        for row in range(self.size):
            for col in range(self.size):
                ch = self.grid.get_cell(row, col)
                positions.setdefault(ch, []).append((row, col))
        return positions

    def _sort_words_by_priority(self, words):
        """
        Ưu tiên từ:
        - ký tự đầu càng hiếm càng ưu tiên
        - từ dài hơn ưu tiên hơn
        """
        def score(w):
            word = w.upper()
            first_freq = self.char_frequency.get(word[0], 10**9)
            return (first_freq, -len(word), word)

        return sorted(words, key=score)

    def _check_word_fits(self, word, row, col, direction):
        dr, dc = direction
        end_row = row + (len(word) - 1) * dr
        end_col = col + (len(word) - 1) * dc
        return 0 <= end_row < self.size and 0 <= end_col < self.size

    def _get_promising_directions(self, word, row, col):
        """
        Lọc hướng triển vọng:
        - Không vượt biên
        - Nếu có ký tự thứ 2 thì phải khớp
        """
        word = word.upper()
        if len(word) == 1:
            return list(range(len(self.directions)))

        result = []
        for dir_idx, direction in enumerate(self.directions):
            if not self._check_word_fits(word, row, col, direction):
                continue
            dr, dc = direction
            nr, nc = row + dr, col + dc
            if self.grid.get_cell(nr, nc) == word[1]:
                result.append(dir_idx)
        return result

    def _heuristic(self, word, row, col, index, direction):
        """
        Heuristic cho Greedy Best-First:
        - remaining: số ký tự còn thiếu
        - lookahead_penalty: phạt nếu 1-2 bước tiếp theo có dấu hiệu mismatch
        """
        remaining = len(word) - index
        dr, dc = direction
        penalty = 0

        lookahead_steps = min(2, remaining)
        for step in range(lookahead_steps):
            check_idx = index + step
            rr = row + (step + 1) * dr
            cc = col + (step + 1) * dc
            if not (0 <= rr < self.size and 0 <= cc < self.size):
                penalty += 3
                continue
            if self.grid.get_cell(rr, cc) != word[check_idx]:
                penalty += 2

        return remaining + penalty

    def _greedy_search_word(self, word, start_candidates):
        """
        Greedy Best-First trên không gian state:
        (row, col, index, direction_idx, path)

        index: số ký tự đã khớp trong word.
        """
        frontier = []
        visited = set()
        tie = 0

        for row, col, dir_idx in start_candidates:
            direction = self.directions[dir_idx]
            h = self._heuristic(word, row, col, 1, direction)
            print(h, row, col)
            heapq.heappush(frontier, (h, tie, row, col, 1, dir_idx, [(row, col)]))
            tie += 1

        while frontier:
            _, _, row, col, index, dir_idx, path = heapq.heappop(frontier)
            state = (row, col, index, dir_idx)
            if state in visited:
                continue
            visited.add(state)
            self.nodes_explored += 1

            if index == len(word):
                return path, dir_idx

            dr, dc = self.directions[dir_idx]
            nr, nc = row + dr, col + dc

            if not (0 <= nr < self.size and 0 <= nc < self.size):
                continue
            if self.grid.get_cell(nr, nc) != word[index]:
                continue

            next_index = index + 1
            next_path = path + [(nr, nc)]
            next_h = self._heuristic(word, nr, nc, next_index, self.directions[dir_idx])
            heapq.heappush(frontier, (next_h, tie, nr, nc, next_index, dir_idx, next_path))
            tie += 1

        return None, None

    def iter_word_search(self, word):
        """
        Stream từng bước tìm 1 từ theo đúng thứ tự pop của frontier (heap).

        Event format:
        - inspect_start: {"type": "inspect_start", "position": (r, c)}
        - pop: {"type": "pop", "position": (r, c), "path": [...], "nodes_explored": n}
        - neighbor: {"type": "neighbor", "position": (r, c)}
        - push: {"type": "push", "position": (r, c), "path": [...], "nodes_explored": n}
        - found: {"type": "found", "result": {...}, "nodes_explored": n}
        - not_found: {"type": "not_found", "nodes_explored": n}
        """
        word = word.upper()
        if not word:
            yield {"type": "not_found", "nodes_explored": self.nodes_explored}
            return

        starts = self.char_positions.get(word[0], [])
        if not starts:
            yield {"type": "not_found", "nodes_explored": self.nodes_explored}
            return

        start_candidates = []
        for row, col in starts:
            yield {"type": "inspect_start", "position": (row, col), "nodes_explored": self.nodes_explored}
            dir_ids = self._get_promising_directions(word, row, col)
            for dir_idx in dir_ids:
                start_candidates.append((row, col, dir_idx))

        if not start_candidates:
            yield {"type": "not_found", "nodes_explored": self.nodes_explored}
            return

        frontier = []
        visited = set()
        tie = 0

        for row, col, dir_idx in start_candidates:
            direction = self.directions[dir_idx]
            h = self._heuristic(word, row, col, 1, direction)
            heapq.heappush(frontier, (h, tie, row, col, 1, dir_idx, [(row, col)]))
            tie += 1

        while frontier:
            _, _, row, col, index, dir_idx, path = heapq.heappop(frontier)
            state = (row, col, index, dir_idx)
            if state in visited:
                continue
            visited.add(state)
            self.nodes_explored += 1

            yield {
                "type": "pop",
                "position": (row, col),
                "path": list(path),
                "direction_idx": dir_idx,
                "nodes_explored": self.nodes_explored,
            }

            if index == len(word):
                result = {
                    "word": word,
                    "start": path[0],
                    "end": path[-1],
                    "direction": self.direction_names[dir_idx],
                    "path": path,
                }
                yield {"type": "found", "result": result, "nodes_explored": self.nodes_explored}
                return

            dr, dc = self.directions[dir_idx]
            nr, nc = row + dr, col + dc

            if 0 <= nr < self.size and 0 <= nc < self.size:
                yield {"type": "neighbor", "position": (nr, nc), "nodes_explored": self.nodes_explored}
            else:
                continue

            if self.grid.get_cell(nr, nc) != word[index]:
                continue

            next_index = index + 1
            next_path = path + [(nr, nc)]
            next_h = self._heuristic(word, nr, nc, next_index, self.directions[dir_idx])
            heapq.heappush(frontier, (next_h, tie, nr, nc, next_index, dir_idx, next_path))
            tie += 1
            yield {
                "type": "push",
                "position": (nr, nc),
                "path": list(next_path),
                "direction_idx": dir_idx,
                "nodes_explored": self.nodes_explored,
            }

        yield {"type": "not_found", "nodes_explored": self.nodes_explored}

    def find_word(self, word, verbose=False):
        """Tìm một từ bằng Greedy Best-First Search."""
        del verbose  # giữ chữ ký tương thích interface
        for event in self.iter_word_search(word):
            if event["type"] == "found":
                return event["result"]
        return None

    def solve(self, verbose=False, step_by_step=False):
        """Giải toàn bộ puzzle bằng Greedy Best-First Search."""
        del verbose, step_by_step  # giữ interface giống solver khác
        self.found_words = {}
        self.nodes_explored = 0

        words = self._sort_words_by_priority(self.grid.words)

        tracemalloc.start()
        start_time = time.time()

        for word in words:
            result = self.find_word(word)
            if result:
                self.found_words[word.upper()] = result

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
