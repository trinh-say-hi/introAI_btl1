"""
GUI Word Search tương tác:
- Chọn đề từ thư mục input ngay trên sidebar
- START / PAUSE / NEXT
- Không có AUTO
- Click từ trên sidebar để highlight riêng đường đi của từ đó
"""
import os
import time
import pygame

from UI.grid import Grid
from UI.solver_registry import get_solver_options


class WordSearchGUI:
    def __init__(self, input_dir):
        pygame.init()

        self.input_dir = input_dir
        self.input_files = self._load_input_files()
        self.selected_problem_idx = 0 if self.input_files else -1
        self.solver_options = get_solver_options()
        self.selected_solver_idx = 0 if self.solver_options else -1

        self.grid = None
        self.solver = None
        self.size = 8
        self.algorithm_name = "HEURISTICS"

        self.colors = {
            "bg": (240, 240, 245),
            "grid_bg": (255, 255, 255),
            "grid_border": (200, 200, 220),
            "normal": (255, 255, 255),
            "searching": (255, 242, 140),
            "current": (255, 205, 110),
            "found": (160, 232, 160),
            "selected_word": (100, 170, 255),
            "neighbor": (230, 230, 255),  # Xanh nhạt cho ô lân cận (DFS)
            "text": (40, 40, 60),
            "header": (60, 60, 120),
            "button": (100, 149, 237),
            "button_hover": (70, 130, 220),
            "button_disabled": (160, 165, 180),
        }

        self.grid_margin = 20
        self.sidebar_width = 430
        self.window_width = 1280
        self.window_height = 760
        self.cell_size = 48

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Word Search - Interactive")

        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.font_tiny = pygame.font.Font(None, 20)
        self.font_cell = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()

        self.is_running = True
        self.state = "idle"  # idle / running / paused / completed
        self.step_iter = None
        self.step_delay = 0.12
        self.last_step_ts = 0.0
        self.start_time = None
        self.elapsed_time = 0.0
        self.nodes_explored = 0

        self.word_items = []
        self.found_words = {}
        self.selected_word = None
        self.current_word = None
        self.current_path = []
        self.searching_positions = set()
        self.neighbor_positions = set()  # DFS: ô lân cận đang xét

        self.problem_rects = []
        self.solver_rects = []
        self.word_rects = []
        self.section_boxes = {}
        self.scroll_offsets = {
            "solvers": 0,
            "problems": 0,
            "words": 0,
        }
        self.buttons = {}

        self._build_layout()
        if self.input_files:
            self._set_problem(0)

    def _load_input_files(self):
        if not os.path.isdir(self.input_dir):
            return []
        files = []
        for name in sorted(os.listdir(self.input_dir)):
            if name.lower().endswith(".txt"):
                files.append(os.path.join(self.input_dir, name))
        return files

    def _build_layout(self):
        grid_width = self.window_width - self.sidebar_width - 2 * self.grid_margin - 30
        grid_height = self.window_height - 180
        cell_by_w = max(20, grid_width // max(1, self.size))
        cell_by_h = max(20, grid_height // max(1, self.size))
        self.cell_size = min(56, max(20, min(cell_by_w, cell_by_h)))
        self.font_cell = pygame.font.Font(None, int(self.cell_size * 0.6))

        y = self.window_height - 68
        w = 120
        h = 40
        x = self.grid_margin
        gap = 12
        self.buttons = {
            "start": pygame.Rect(x, y, w, h),
            "pause": pygame.Rect(x + w + gap, y, w, h),
            "next": pygame.Rect(x + (w + gap) * 2, y, w, h),
        }

    def _set_problem(self, idx):
        if not (0 <= idx < len(self.input_files)):
            return
        grid = Grid()
        grid.load_from_file(self.input_files[idx])
        solver = self._build_solver(grid)

        self.grid = grid
        self.solver = solver
        self.size = grid.size
        self.algorithm_name = solver.__class__.__name__.replace("WordSearch", "").upper()
        self.selected_problem_idx = idx
        self._reset_solution_data()
        self._build_layout()
        self._sync_word_items()
        self.scroll_offsets["words"] = 0

    def _build_solver(self, grid):
        if not self.solver_options:
            raise ValueError("Không có solver nào trong registry.")
        _, solver_cls = self.solver_options[self.selected_solver_idx]
        solver = solver_cls(grid)
        self._validate_solver(solver)
        return solver

    def _validate_solver(self, solver):
        if not hasattr(solver, "directions") or not hasattr(solver, "direction_names"):
            raise ValueError("Solver phải có directions và direction_names.")
        if len(solver.directions) != len(solver.direction_names):
            raise ValueError("directions và direction_names phải cùng số phần tử.")

    def _change_solver(self, solver_idx):
        if not (0 <= solver_idx < len(self.solver_options)):
            return
        if solver_idx == self.selected_solver_idx:
            return
        self.selected_solver_idx = solver_idx
        if self.selected_problem_idx >= 0:
            self._set_problem(self.selected_problem_idx)

    def _visible_rows(self, box_height, item_height=24, padding=6):
        usable = max(0, box_height - padding * 2)
        return max(1, usable // item_height)

    def _clamp_offset(self, key, total_count, visible_count):
        max_offset = max(0, total_count - visible_count)
        self.scroll_offsets[key] = max(0, min(self.scroll_offsets[key], max_offset))

    def _truncate_text(self, text, max_width):
        if self.font_tiny.size(text)[0] <= max_width:
            return text
        suffix = "..."
        keep = text
        while keep and self.font_tiny.size(keep + suffix)[0] > max_width:
            keep = keep[:-1]
        return keep + suffix

    def _reset_solution_data(self):
        self.state = "idle"
        self.step_iter = None
        self.last_step_ts = 0.0
        self.start_time = None
        self.elapsed_time = 0.0
        self.nodes_explored = 0
        self.found_words = {}
        self.selected_word = None
        self.current_word = None
        self.current_path = []
        self.searching_positions = set()
        self.neighbor_positions = set()

    def _sync_word_items(self):
        self.word_items = []
        for word in self.grid.words:
            self.word_items.append(
                {
                    "word": word.upper(),
                    "found": False,
                    "path": [],
                    "start": None,
                    "end": None,
                    "direction": None,
                }
            )

    def _get_word_item(self, word):
        for item in self.word_items:
            if item["word"] == word:
                return item
        return None

    def _start(self):
        if not self.grid:
            return
        self._reset_solution_data()
        self._sync_word_items()
        self.state = "running"
        self.start_time = time.time()
        self.step_iter = self._step_generator()

    def _toggle_pause(self):
        if self.state == "running":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "running"

    def _next(self):
        if self.state == "paused":
            self._advance_step()

    def _advance_step(self):
        if not self.step_iter:
            return
        try:
            status = next(self.step_iter)
            if status == "done":
                self.state = "completed"
                self.step_iter = None
                if self.start_time:
                    self.elapsed_time = time.time() - self.start_time
        except StopIteration:
            self.state = "completed"
            self.step_iter = None

    def _step_generator(self):
        words = self._get_ordered_words()

        for word in words:
            word_u = word.upper()
            self.current_word = word_u
            found = False

            starts = self._get_start_positions(word_u)

            for row, col in starts:
                if found:
                    break
                self.searching_positions = {(row, col)}
                self.current_path = [(row, col)]
                yield "step"

                dir_ids = self._get_direction_candidates(word_u, row, col)

                for dir_idx in dir_ids:
                    direction = self.solver.directions[dir_idx]
                    dr, dc = direction
                    
                    # DFS: Hiển thị ô lân cận theo hướng đang xét
                    next_r = row + dr
                    next_c = col + dc
                    if hasattr(self.solver, 'get_neighbor_positions') and 0 <= next_r < self.size and 0 <= next_c < self.size:
                        self.neighbor_positions = {(next_r, next_c)}
                        yield "step"
                    
                    # Clear neighbor sau khi hiển thị
                    self.neighbor_positions = set()
                    
                    if not self._check_word_fits(word_u, row, col, direction):
                        continue

                    cur_r, cur_c = row, col
                    path = [(row, col)]
                    match = True

                    for i in range(1, len(word_u)):
                        cur_r += dr
                        cur_c += dc
                        self.nodes_explored += 1

                        if not (0 <= cur_r < self.size and 0 <= cur_c < self.size):
                            match = False
                            break
                        if self.grid.get_cell(cur_r, cur_c) != word_u[i]:
                            match = False
                            break

                        path.append((cur_r, cur_c))
                        self.current_path = list(path)
                        self.searching_positions = {(cur_r, cur_c)}
                        yield "step"

                    if match and len(path) == len(word_u):
                        info = {
                            "path": list(path),
                            "start": path[0],
                            "end": path[-1],
                            "direction": self.solver.direction_names[dir_idx],
                        }
                        self.found_words[word_u] = info
                        item = self._get_word_item(word_u)
                        if item:
                            item["found"] = True
                            item["path"] = list(path)
                            item["start"] = path[0]
                            item["end"] = path[-1]
                            item["direction"] = info["direction"]
                        if self.selected_word is None:
                            self.selected_word = word_u
                        self.current_path = list(path)
                        self.searching_positions = set()
                        yield "step"
                        found = True
                        break

            self.current_path = []
            self.searching_positions = set()
            yield "step"

        self.current_word = None
        self.current_path = []
        self.searching_positions = set()
        yield "done"

    def _get_ordered_words(self):
        words = self.grid.words
        if hasattr(self.solver, "_sort_words_by_priority"):
            return self.solver._sort_words_by_priority(words)
        return words

    def _get_start_positions(self, word):
        if hasattr(self.solver, "char_positions"):
            return self.solver.char_positions.get(word[0], [])
        positions = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid.get_cell(r, c) == word[0]:
                    positions.append((r, c))
        return positions

    def _get_direction_candidates(self, word, row, col):
        if hasattr(self.solver, "_get_promising_directions"):
            return self.solver._get_promising_directions(word, row, col)
        return list(range(len(self.solver.directions)))

    def _check_word_fits(self, word, row, col, direction):
        if hasattr(self.solver, "_check_word_fits"):
            return self.solver._check_word_fits(word, row, col, direction)
        dr, dc = direction
        end_row = row + (len(word) - 1) * dr
        end_col = col + (len(word) - 1) * dc
        return 0 <= end_row < self.size and 0 <= end_col < self.size

    def _draw_button(self, name, text, enabled):
        rect = self.buttons[name]
        hover = rect.collidepoint(pygame.mouse.get_pos()) and enabled
        color = self.colors["button_hover"] if hover else self.colors["button"]
        if not enabled:
            color = self.colors["button_disabled"]
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.colors["grid_border"], rect, 2, border_radius=8)
        label = self.font_small.render(text, True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_grid(self):
        x0 = self.grid_margin
        y0 = 80
        w = self.size * self.cell_size
        h = self.size * self.cell_size

        pygame.draw.rect(self.screen, self.colors["grid_bg"], (x0 - 5, y0 - 5, w + 10, h + 10), border_radius=10)

        found_positions = set()
        for item in self.word_items:
            if item["found"]:
                found_positions.update(item["path"])

        selected_path = set()
        selected_item = self._get_word_item(self.selected_word) if self.selected_word else None
        if selected_item and selected_item["found"]:
            selected_path = set(selected_item["path"])

        for r in range(self.size):
            for c in range(self.size):
                x = x0 + c * self.cell_size
                y = y0 + r * self.cell_size
                pos = (r, c)
                color = self.colors["normal"]
                border = 1

                if pos in found_positions:
                    color = self.colors["found"]
                    border = 2
                if pos in selected_path:
                    color = self.colors["selected_word"]
                    border = 3
                # DFS: Ô lân cận đang xét (màu xanh nhạt)
                if pos in self.neighbor_positions:
                    color = self.colors["neighbor"]
                    border = 2
                if pos in self.current_path:
                    color = self.colors["current"]
                    border = 3
                if pos in self.searching_positions:
                    color = self.colors["searching"]
                    border = 3

                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, self.colors["grid_border"], (x, y, self.cell_size, self.cell_size), border)
                ch = self.grid.grid[r][c]
                text = self.font_cell.render(ch, True, self.colors["text"])
                self.screen.blit(text, text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2)))

    def _draw_sidebar(self):
        sx = self.window_width - self.sidebar_width
        sy = 12
        sh = self.window_height - 24
        pygame.draw.rect(self.screen, (250, 250, 255), (sx, sy, self.sidebar_width - 12, sh), border_radius=10)

        self.problem_rects = []
        self.solver_rects = []
        self.word_rects = []
        self.section_boxes = {}

        inner_x = sx + 14
        inner_w = self.sidebar_width - 40
        y = sy + 12

        title_h = 22
        section_gap = 10
        solver_h = 120
        problem_h = 150
        info_h = 150
        words_h = max(120, sh - (title_h * 3 + solver_h + problem_h + info_h + section_gap * 5 + 24))

        # Section: Solvers
        t = self.font_medium.render("Thuat toan (click):", True, self.colors["header"])
        self.screen.blit(t, (inner_x, y))
        y += title_h
        solver_box = pygame.Rect(inner_x, y, inner_w, solver_h)
        self.section_boxes["solvers"] = solver_box
        pygame.draw.rect(self.screen, (245, 246, 252), solver_box, border_radius=8)

        solver_visible = self._visible_rows(solver_h, item_height=24)
        self._clamp_offset("solvers", len(self.solver_options), solver_visible)
        start = self.scroll_offsets["solvers"]
        end = min(len(self.solver_options), start + solver_visible)

        old_clip = self.screen.get_clip()
        self.screen.set_clip(solver_box)
        row_y = solver_box.y + 6
        for idx in range(start, end):
            name, _ = self.solver_options[idx]
            rect = pygame.Rect(solver_box.x + 6, row_y, solver_box.w - 12, 22)
            if idx == self.selected_solver_idx:
                pygame.draw.rect(self.screen, (220, 232, 255), rect, border_radius=4)
            short_name = self._truncate_text(f"{idx + 1}. {name}", rect.w - 8)
            line = self.font_tiny.render(short_name, True, self.colors["text"])
            self.screen.blit(line, (rect.x + 4, rect.y + 3))
            self.solver_rects.append((idx, rect))
            row_y += 24
        self.screen.set_clip(old_clip)
        y += solver_h + section_gap

        # Section: Problems
        t = self.font_medium.render("De bai (click):", True, self.colors["header"])
        self.screen.blit(t, (inner_x, y))
        y += title_h
        problem_box = pygame.Rect(inner_x, y, inner_w, problem_h)
        self.section_boxes["problems"] = problem_box
        pygame.draw.rect(self.screen, (245, 246, 252), problem_box, border_radius=8)

        prob_visible = self._visible_rows(problem_h, item_height=24)
        self._clamp_offset("problems", len(self.input_files), prob_visible)
        start = self.scroll_offsets["problems"]
        end = min(len(self.input_files), start + prob_visible)

        old_clip = self.screen.get_clip()
        self.screen.set_clip(problem_box)
        row_y = problem_box.y + 6
        for idx in range(start, end):
            path = self.input_files[idx]
            rect = pygame.Rect(problem_box.x + 6, row_y, problem_box.w - 12, 22)
            if idx == self.selected_problem_idx:
                pygame.draw.rect(self.screen, (220, 232, 255), rect, border_radius=4)
            label = f"{idx + 1}. {os.path.basename(path)}"
            short_label = self._truncate_text(label, rect.w - 8)
            line = self.font_tiny.render(short_label, True, self.colors["text"])
            self.screen.blit(line, (rect.x + 4, rect.y + 3))
            self.problem_rects.append((idx, rect))
            row_y += 24
        self.screen.set_clip(old_clip)
        y += problem_h + section_gap

        # Section: Words
        t = self.font_medium.render("Tu can tim (click):", True, self.colors["header"])
        self.screen.blit(t, (inner_x, y))
        y += title_h
        words_box = pygame.Rect(inner_x, y, inner_w, words_h)
        self.section_boxes["words"] = words_box
        pygame.draw.rect(self.screen, (245, 246, 252), words_box, border_radius=8)

        words_visible = self._visible_rows(words_h, item_height=23)
        self._clamp_offset("words", len(self.word_items), words_visible)
        start = self.scroll_offsets["words"]
        end = min(len(self.word_items), start + words_visible)

        old_clip = self.screen.get_clip()
        self.screen.set_clip(words_box)
        row_y = words_box.y + 6
        for idx in range(start, end):
            item = self.word_items[idx]
            rect = pygame.Rect(words_box.x + 6, row_y, words_box.w - 12, 22)
            if self.selected_word == item["word"]:
                pygame.draw.rect(self.screen, (210, 226, 255), rect, border_radius=4)
            prefix = "[x]" if item["found"] else "[ ]"
            color = (34, 139, 34) if item["found"] else self.colors["text"]
            label = self._truncate_text(f"{prefix} {item['word']}", rect.w - 8)
            line = self.font_tiny.render(label, True, color)
            self.screen.blit(line, (rect.x + 4, rect.y + 3))
            self.word_rects.append((item["word"], rect))
            row_y += 23
        self.screen.set_clip(old_clip)
        y += words_h + section_gap

        # Section: Info
        info = [
            f"Trang thai: {self.state.upper()}",
            f"Dang tim: {self.current_word or '-'}",
            f"Da tim: {len(self.found_words)}/{len(self.word_items)}",
            f"Thoi gian: {self.elapsed_time:.2f}s",
            f"So node: {self.nodes_explored}",
        ]
        sel = self._get_word_item(self.selected_word) if self.selected_word else None
        if sel and sel["found"]:
            info.extend(
                [
                    f"Word: {sel['word']}",
                    f"Start: {sel['start']}",
                    f"End: {sel['end']}",
                    f"Dir: {sel['direction']}",
                ]
            )

        info_box = pygame.Rect(inner_x, y, inner_w, info_h)
        pygame.draw.rect(self.screen, (245, 246, 252), info_box, border_radius=8)
        line_y = info_box.y + 6
        for line in info:
            if line_y > info_box.bottom - 18:
                break
            txt = self.font_tiny.render(self._truncate_text(line, info_box.w - 12), True, self.colors["text"])
            self.screen.blit(txt, (info_box.x + 6, line_y))
            line_y += 20

    def _draw_header(self):
        title = self.font_large.render(f"WORD SEARCH - {self.algorithm_name}", True, self.colors["header"])
        self.screen.blit(title, (self.grid_margin, 24))
        hint = self.font_tiny.render("Space: pause/resume | Right: next step | Esc: exit", True, self.colors["text"])
        self.screen.blit(hint, (self.grid_margin, self.window_height - 96))

    def _draw_controls(self):
        self._draw_button("start", "START", enabled=self.grid is not None)
        pause_text = "RESUME" if self.state == "paused" else "PAUSE"
        self._draw_button("pause", pause_text, enabled=self.state in ("running", "paused"))
        self._draw_button("next", "NEXT", enabled=self.state == "paused")

    def _render(self):
        self.screen.fill(self.colors["bg"])
        if self.grid:
            self._draw_grid()
        self._draw_header()
        self._draw_controls()
        self._draw_sidebar()
        pygame.display.flip()

    def _handle_click(self, pos):
        if self.buttons["start"].collidepoint(pos):
            self._start()
            return
        if self.buttons["pause"].collidepoint(pos):
            self._toggle_pause()
            return
        if self.buttons["next"].collidepoint(pos):
            self._next()
            return

        for idx, rect in self.solver_rects:
            if rect.collidepoint(pos):
                self._change_solver(idx)
                return

        for idx, rect in self.problem_rects:
            if rect.collidepoint(pos):
                self._set_problem(idx)
                return

        for word, rect in self.word_rects:
            if rect.collidepoint(pos):
                self.selected_word = word
                return

    def _handle_scroll(self, mouse_pos, scroll_y):
        # pygame wheel: y > 0 là cuộn lên, y < 0 là cuộn xuống
        delta = -scroll_y
        for key, rect in self.section_boxes.items():
            if rect.collidepoint(mouse_pos):
                if key == "solvers":
                    visible = self._visible_rows(rect.h, item_height=24)
                    total = len(self.solver_options)
                elif key == "problems":
                    visible = self._visible_rows(rect.h, item_height=24)
                    total = len(self.input_files)
                else:
                    visible = self._visible_rows(rect.h, item_height=23)
                    total = len(self.word_items)

                self.scroll_offsets[key] += delta
                self._clamp_offset(key, total, visible)
                return

    def _update(self):
        if self.start_time and self.state in ("running", "paused"):
            self.elapsed_time = time.time() - self.start_time

        if self.state == "running":
            now = time.time()
            if now - self.last_step_ts >= self.step_delay:
                self.last_step_ts = now
                self._advance_step()

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    elif event.key == pygame.K_SPACE:
                        self._toggle_pause()
                    elif event.key == pygame.K_RIGHT:
                        self._next()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEWHEEL:
                    self._handle_scroll(pygame.mouse.get_pos(), event.y)

            self._update()
            self._render()
            self.clock.tick(60)
        pygame.quit()


def run_gui(input_dir):
    gui = WordSearchGUI(input_dir=input_dir)
    gui.run()
