import pygame

class Visualizer:
    def __init__(self, size, window_width=600):
        self.size = size
        self.grid_width = window_width
        self.sidebar_width = 250
        self.total_width = self.grid_width + self.sidebar_width
        self.cell_size = self.grid_width // size

        self.screen = pygame.display.set_mode((self.total_width, self.grid_width + 120))
        pygame.display.set_caption(f"Killer sudoku Solver {size}x{size} - A* Visualization")

        self.font_size = int(self.cell_size * 0.5)
        self.small_font_size = int(self.font_size * 0.35)
        self.font = pygame.font.SysFont("Arial", int(self.cell_size * 0.5))
        self.small_font = pygame.font.SysFont("Arial", self.small_font_size)
        self.info_font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 22, bold=True)

    def draw_grid(self, board, highlight_cell=None):
        self.screen.fill((255, 255, 255), (0, 0, self.grid_width, self.grid_width + 120))

        if highlight_cell:
            row, col = highlight_cell
            rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (255, 255, 200), rect)

        subgrid = int(self.size**0.5)
        for i in range(self.size + 1):
            thickness = 4 if i % subgrid == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.grid_width, i * self.cell_size), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.grid_width), thickness)

        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] != 0:
                    color = (230, 0, 0) if highlight_cell == (row, col) else (0, 0, 0)
                    text = self.font.render(str(board[row][col]), True, color)
                    text_rect = text.get_rect(center=(col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

    def draw_dashed_line(self, start, end, color=(150, 150, 150)):
        dist = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
        dash_len = 3
        for i in range(0, int(dist), dash_len * 2):
            s = (start[0] + (end[0] - start[0]) * (i / dist), start[1] + (end[1] - start[1]) * (i / dist))
            e = (start[0] + (end[0] - start[0]) * ((i + dash_len) / dist), start[1] + (end[1] - start[1]) * ((i + dash_len) / dist))
            pygame.draw.line(self.screen, color, s, e, 2)

    def draw_cages(self, cages):
        cage_map = {}
        for i, cage in enumerate(cages):
            for cell in cage.cells:
                cage_map[cell] = i

        for i, cage in enumerate(cages):
            first_cell = min(cage.cells)
            text = self.small_font.render(str(cage.target_sum), True, (70, 70, 70))
            self.screen.blit(text, (first_cell[1] * self.cell_size + 5, first_cell[0] * self.cell_size + 5))

            for row, col in cage.cells:
                x, y = col * self.cell_size, row * self.cell_size
                # tren
                if (row - 1, col) not in cage_map or cage_map[(row - 1, col)] != i:
                    self.draw_dashed_line((x + 4, y + 4), (x +  self.cell_size - 4, y + 4))
                # duoi
                if (row + 1, col) not in cage_map or cage_map[(row + 1, col)] != i:
                    self.draw_dashed_line((x + 4, y + self.cell_size - 4), (x +  self.cell_size - 4, y + self.cell_size - 4))
                # trai
                if (row, col - 1) not in cage_map or cage_map[(row, col - 1)] != i:
                    self.draw_dashed_line((x + 4, y + 4), (x - 4, y + self.cell_size - 4))
                # phai
                if (row, col + 1) not in cage_map or cage_map[(row, col + 1)] != i:
                    self.draw_dashed_line((x + self.cell_size - 4, y + 4), (x + self.cell_size - 4, y + self.cell_size - 4))
                    
    def draw_info(self, nodes, speed, is_paused):
        y_offset = self.grid_width + 10
        status = "PAUSED" if is_paused else "RUNNING"
        text = self.info_font.render(f"Nodes: {nodes} | Delay: {speed:.2f}s | Status: {status}", True, (0, 0, 0))
        self.screen.blit(text, (10, y_offset))

        instructions = "SPACE: Start | P: Pause/Resume | UP/DOWN: Speed | ESC: Quit"
        instr_text = self.info_font.render(instructions, True, (100, 100, 100))
        self.screen.blit(instr_text, (10, y_offset + 30))

    def draw_sidebar(self, algos, selected_algo, files, selected_file):
        sidebar_rect = pygame.Rect(self.grid_width, 0, self.sidebar_width, self.grid_width + 120)
        pygame.draw.rect(self.screen, (240, 240, 245), sidebar_rect)
        pygame.draw.line(self.screen, (200, 200, 200), (self.grid_width, 0), (self.grid_width, self.grid_width + 120), 2)

        y = 20
        lbl1 = self.title_font.render("Giải thuật:", True, (50, 50, 50))
        self.screen.blit(lbl1, (self.grid_width + 20, y))
        y += 40

        algo_rects = {}
        for algo in algos:
            color = (0, 102, 204) if algo == selected_algo else (100, 100, 100)
            bg = (215, 230, 250) if algo == selected_algo else (230, 230, 230)
            rect = pygame.Rect(self.grid_width + 20, y, self.sidebar_width - 40, 35)
            pygame.draw.rect(self.screen, bg, rect, border_radius=5)
            txt = self.info_font.render(algo, True, color)
            self.screen.blit(txt, (self.grid_width + 30, y + 5))
            algo_rects[algo] = rect
            y += 45

        y += 20

        lbl2 = self.title_font.render("Test cases (input):", True, (50, 50, 50))
        self.screen.blit(lbl2, (self.grid_width + 20, y))
        y += 40

        file_rects = {}
        for f in files:
            color = (0, 102, 204) if f == selected_file else (100, 100, 100)
            bg = (215, 230, 250) if f == selected_file else (230, 230, 230)
            rect = pygame.Rect(self.grid_width + 20, y, self.sidebar_width - 40, 30)
            pygame.draw.rect(self.screen, bg, rect, border_radius=5)
            txt = self.info_font.render(f, True, color)
            self.screen.blit(txt, (self.grid_width + 30, y + 2))
            file_rects[f] = rect
            y += 35

        return algo_rects, file_rects