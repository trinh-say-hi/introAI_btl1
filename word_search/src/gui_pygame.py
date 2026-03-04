"""
GUI pygame cho Word Search - Demo step-by-step trực quan
"""
import pygame
import sys
import time

class WordSearchGUI:
    def __init__(self, grid, solver):
        """
        Khởi tạo GUI
        Args:
            grid: đối tượng Grid
            solver: đối tượng WordSearchDFS
        """
        pygame.init()
        
        self.grid = grid
        self.solver = solver
        self.size = grid.size
        
        # Màu sắc
        self.COLORS = {
            'background': (240, 240, 245),
            'grid_bg': (255, 255, 255),
            'grid_border': (200, 200, 220),
            'cell_normal': (255, 255, 255),
            'cell_searching': (255, 255, 150),
            'cell_found': (144, 238, 144),
            'cell_current': (255, 200, 100),
            'cell_checking': (255, 180, 180),  # Màu đỏ nhạt khi check
            'cell_failed': (255, 220, 220),    # Màu hồng nhạt khi fail
            'text': (40, 40, 60),
            'header': (60, 60, 120),
            'success': (34, 139, 34),
            'error': (220, 20, 60),
            'info_bg': (250, 250, 255),
            'button': (100, 149, 237),
            'button_hover': (70, 130, 220)
        }
        
        # Kích thước - scale cho laptop 14 inch (max ~900px)
        if self.size <= 8:
            self.CELL_SIZE = 50
        elif self.size <= 10:
            self.CELL_SIZE = 42
        else:  # 12x12
            self.CELL_SIZE = 38
        
        self.GRID_MARGIN = 15
        self.SIDEBAR_WIDTH = 300
        
        grid_width = self.size * self.CELL_SIZE + 2 * self.GRID_MARGIN
        grid_height = self.size * self.CELL_SIZE + 2 * self.GRID_MARGIN
        
        self.WINDOW_WIDTH = grid_width + self.SIDEBAR_WIDTH + 30
        self.WINDOW_HEIGHT = grid_height + 150
        
        # Tạo cửa sổ
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Word Search Solver - DFS Algorithm")
        
        # Icon (optional)
        try:
            icon = pygame.Surface((32, 32))
            icon.fill(self.COLORS['button'])
            pygame.display.set_icon(icon)
        except:
            pass
        
        # Font
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.font_cell = pygame.font.Font(None, int(self.CELL_SIZE * 0.6))
        
        # Trạng thái
        self.found_words = {}
        self.current_word = None
        self.current_path = []
        self.searching_positions = set()
        self.checking_position = None  # Ô đang check
        self.failed_positions = set()  # Các ô check thất bại
        self.animation_speed = 0.3
        self.is_running = True
        self.is_paused = False
        self.is_auto_play = False
        
        # Thống kê
        self.start_time = None
        self.elapsed_time = 0
        self.nodes_explored = 0
        
        # Buttons
        self.buttons = self.create_buttons()
        
        self.clock = pygame.time.Clock()
    
    def create_buttons(self):
        """Tạo các nút điều khiển"""
        button_y = self.WINDOW_HEIGHT - 70
        button_height = 40
        button_width = 100
        spacing = 10
        
        start_x = (self.WINDOW_WIDTH - self.SIDEBAR_WIDTH) // 2 - (button_width * 2 + spacing) // 2
        
        return {
            'start': pygame.Rect(start_x, button_y, button_width, button_height),
            'pause': pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height),
            'next': pygame.Rect(start_x + (button_width + spacing) * 2, button_y, button_width, button_height),
            'auto': pygame.Rect(start_x + (button_width + spacing) * 3, button_y, button_width, button_height)
        }
    
    def draw_button(self, rect, text, color, hover=False):
        """Vẽ nút bấm"""
        button_color = self.COLORS['button_hover'] if hover else color
        pygame.draw.rect(self.screen, button_color, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLORS['grid_border'], rect, 2, border_radius=8)
        
        # Dùng ASCII cho buttons để tránh lỗi font
        text_surf = self.font_small.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def draw_grid(self):
        """Vẽ lưới Word Search"""
        # Background
        grid_x = self.GRID_MARGIN
        grid_y = 80
        grid_width = self.size * self.CELL_SIZE
        grid_height = self.size * self.CELL_SIZE
        
        pygame.draw.rect(self.screen, self.COLORS['grid_bg'],
                        (grid_x - 5, grid_y - 5, grid_width + 10, grid_height + 10),
                        border_radius=10)
        
        # Vẽ các ô
        for i in range(self.size):
            for j in range(self.size):
                x = grid_x + j * self.CELL_SIZE
                y = grid_y + i * self.CELL_SIZE
                
                # Chọn màu cho ô
                cell_color = self.COLORS['cell_normal']
                border_width = 1
                
                # Ưu tiên: checking > failed > searching > current > found > normal
                if self.checking_position and (i, j) == self.checking_position:
                    cell_color = self.COLORS['cell_checking']
                    border_width = 3
                elif (i, j) in self.failed_positions:
                    cell_color = self.COLORS['cell_failed']
                    border_width = 2
                elif (i, j) in self.searching_positions:
                    cell_color = self.COLORS['cell_searching']
                    border_width = 2
                elif (i, j) in self.current_path:
                    cell_color = self.COLORS['cell_current']
                    border_width = 3
                else:
                    # Kiểm tra xem có thuộc từ đã tìm thấy không
                    for word_info in self.found_words.values():
                        if (i, j) in word_info['path']:
                            cell_color = self.COLORS['cell_found']
                            border_width = 2
                            break
                
                # Vẽ ô
                pygame.draw.rect(self.screen, cell_color,
                               (x, y, self.CELL_SIZE, self.CELL_SIZE))
                pygame.draw.rect(self.screen, self.COLORS['grid_border'],
                               (x, y, self.CELL_SIZE, self.CELL_SIZE), border_width)
                
                # Vẽ chữ
                char = self.grid.grid[i][j]
                text_surf = self.font_cell.render(char, True, self.COLORS['text'])
                text_rect = text_surf.get_rect(center=(x + self.CELL_SIZE // 2,
                                                       y + self.CELL_SIZE // 2))
                self.screen.blit(text_surf, text_rect)
    
    def draw_sidebar(self):
        """Vẽ thanh thông tin bên phải"""
        sidebar_x = self.WINDOW_WIDTH - self.SIDEBAR_WIDTH
        sidebar_y = 80
        
        # Background
        pygame.draw.rect(self.screen, self.COLORS['info_bg'],
                        (sidebar_x, sidebar_y, self.SIDEBAR_WIDTH - 20, self.WINDOW_HEIGHT - 160),
                        border_radius=10)
        
        y_offset = sidebar_y + 20
        
        # Từ đang tìm
        title = self.font_medium.render("Current Word:", True, self.COLORS['header'])
        self.screen.blit(title, (sidebar_x + 20, y_offset))
        y_offset += 40
        
        if self.current_word:
            word_text = self.font_large.render(self.current_word, True, self.COLORS['error'])
            self.screen.blit(word_text, (sidebar_x + 20, y_offset))
        else:
            word_text = self.font_large.render("---", True, self.COLORS['text'])
            self.screen.blit(word_text, (sidebar_x + 20, y_offset))
        
        y_offset += 70
        
        # Hiển thị progress bar
        progress_title = self.font_medium.render("Progress:", True, self.COLORS['header'])
        self.screen.blit(progress_title, (sidebar_x + 20, y_offset))
        y_offset += 35
        
        # Progress bar
        bar_width = self.SIDEBAR_WIDTH - 60
        bar_height = 30
        bar_x = sidebar_x + 20
        
        # Background bar
        pygame.draw.rect(self.screen, (220, 220, 220),
                        (bar_x, y_offset, bar_width, bar_height), border_radius=5)
        
        # Progress bar
        if len(self.grid.words) > 0:
            progress = len(self.found_words) / len(self.grid.words)
            fill_width = int(bar_width * progress)
            pygame.draw.rect(self.screen, self.COLORS['success'],
                            (bar_x, y_offset, fill_width, bar_height), border_radius=5)
        
        # Progress text
        progress_text = f"{len(self.found_words)} / {len(self.grid.words)}"
        text_surf = self.font_medium.render(progress_text, True, self.COLORS['text'])
        text_rect = text_surf.get_rect(center=(bar_x + bar_width // 2, y_offset + bar_height // 2))
        self.screen.blit(text_surf, text_rect)
        
        y_offset += 50
        
        # Thống kê
        y_offset = self.WINDOW_HEIGHT - 280
        pygame.draw.rect(self.screen, self.COLORS['grid_bg'],
                        (sidebar_x + 10, y_offset, self.SIDEBAR_WIDTH - 40, 180),
                        border_radius=8)
        
        y_offset += 15
        
        stats_title = self.font_medium.render("Statistics:", True, self.COLORS['header'])
        self.screen.blit(stats_title, (sidebar_x + 20, y_offset))
        y_offset += 35
        
        # Cập nhật thời gian theo thời gian thực
        if self.start_time is not None:
            self.elapsed_time = time.time() - self.start_time
        
        stats = [
            f"Found: {len(self.found_words)}/{len(self.grid.words)} words",
            f"Time: {self.elapsed_time:.2f} seconds"
        ]
        
        for stat in stats:
            text = self.font_small.render(stat, True, self.COLORS['text'])
            self.screen.blit(text, (sidebar_x + 30, y_offset))
            y_offset += 28
    
    def draw_header(self):
        """Vẽ tiêu đề"""
        title = self.font_large.render("WORD SEARCH SOLVER - DFS", True, self.COLORS['header'])
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
    
    def draw_buttons(self):
        """Vẽ các nút điều khiển"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Start button
        hover = self.buttons['start'].collidepoint(mouse_pos)
        self.draw_button(self.buttons['start'], "START", self.COLORS['success'], hover)
        
        # Pause button
        hover = self.buttons['pause'].collidepoint(mouse_pos)
        text = "RESUME" if self.is_paused else "PAUSE"
        self.draw_button(self.buttons['pause'], text, self.COLORS['button'], hover)
        
        # Next button
        hover = self.buttons['next'].collidepoint(mouse_pos)
        self.draw_button(self.buttons['next'], "NEXT", self.COLORS['button'], hover)
        
        # Auto button
        hover = self.buttons['auto'].collidepoint(mouse_pos)
        text = "STOP" if self.is_auto_play else "AUTO"
        self.draw_button(self.buttons['auto'], text, self.COLORS['error'] if self.is_auto_play else self.COLORS['button'], hover)
    
    def handle_events(self):
        """Xử lý sự kiện"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.buttons['start'].collidepoint(mouse_pos):
                    self.start_solving()
                elif self.buttons['pause'].collidepoint(mouse_pos):
                    self.is_paused = not self.is_paused
                elif self.buttons['next'].collidepoint(mouse_pos):
                    # Auto pause if not paused yet, then step
                    if not self.is_paused:
                        self.is_paused = True
                    return 'next_step'
                elif self.buttons['auto'].collidepoint(mouse_pos):
                    self.is_auto_play = not self.is_auto_play
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused
                elif event.key == pygame.K_RIGHT:
                    # Auto pause if not paused yet, then step
                    if not self.is_paused:
                        self.is_paused = True
                    return 'next_step'
                elif event.key == pygame.K_a:
                    self.is_auto_play = not self.is_auto_play
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def start_solving(self):
        """Bắt đầu giải"""
        self.start_time = time.time()
        self.found_words = {}
        self.nodes_explored = 0
    
    def animate_search(self, word, row, col, direction_idx):
        """Animation tìm kiếm một từ theo hướng"""
        direction = self.solver.directions[direction_idx]
        dr, dc = direction
        
        path = [(row, col)]
        current_row, current_col = row, col
        
        for i in range(1, len(word)):
            # Move to next cell
            current_row += dr
            current_col += dc
            
            # Kiểm tra vị trí có hợp lệ không
            if not (0 <= current_row < self.size and 0 <= current_col < self.size):
                # Hiển thị fail (out of bounds)
                self.checking_position = None
                self.render()
                if not self.is_auto_play:
                    pygame.time.wait(int(self.animation_speed * 500))
                break
            
            # Hiệu ứng: Đang check ô này (màu đỏ nhạt)
            self.current_word = word
            self.current_path = path.copy()
            self.checking_position = (current_row, current_col)
            self.searching_positions = set()
            
            self.render()
            
            # Wait for animation
            if not self.is_auto_play:
                pygame.time.wait(int(self.animation_speed * 500))
            
            # Check events
            result = self.handle_events()
            if result == False:
                return False
            
            # Handle pause - wait until resume or next
            while self.is_paused and result != 'next_step':
                self.render()
                result = self.handle_events()
                if result == False:
                    return False
                pygame.time.wait(50)
            
            # If next_step, continue once then pause again
            if result == 'next_step':
                self.is_paused = True
            
            # Kiểm tra ký tự có khớp không
            if self.grid.get_cell(current_row, current_col) != word[i]:
                # KHÔNG KHỚP - Hiển thị fail (màu hồng nhạt)
                self.failed_positions.add((current_row, current_col))
                self.checking_position = None
                self.render()
                if not self.is_auto_play:
                    pygame.time.wait(int(self.animation_speed * 500))
                
                # Xóa failed sau 1 chút
                self.failed_positions.discard((current_row, current_col))
                break
            
            # KHỚP - Thêm vào path (màu cam)
            path.append((current_row, current_col))
            self.nodes_explored += 1
            self.checking_position = None
            self.current_path = path.copy()
            
            self.render()
            if not self.is_auto_play:
                pygame.time.wait(int(self.animation_speed * 300))
        
        self.checking_position = None
        return path if len(path) == len(word) else None
    
    def solve_step_by_step(self):
        """Giải từng bước với animation"""
        self.start_solving()
        
        for word in self.grid.words:
            self.current_word = word
            found = False
            
            for i in range(self.size):
                if found:
                    break
                
                for j in range(self.size):
                    if found:
                        break
                    
                    if self.grid.get_cell(i, j) == word[0]:
                        self.searching_positions = {(i, j)}
                        self.render()
                        
                        if not self.is_auto_play:
                            pygame.time.wait(int(self.animation_speed * 500))
                        
                        for dir_idx in range(8):
                            result = self.animate_search(word, i, j, dir_idx)
                            
                            if result == False:
                                return False
                            
                            if result and len(result) == len(word):
                                self.found_words[word] = {
                                    'path': result,
                                    'start': (i, j),
                                    'end': result[-1],
                                    'direction': self.solver.direction_names[dir_idx]
                                }
                                found = True
                                
                                # Hiển thị tìm thấy
                                self.current_path = result
                                self.render()
                                pygame.time.wait(800)
                                break
            
            self.current_path = []
            self.searching_positions = set()
        
        # Kết thúc
        self.current_word = None
        self.elapsed_time = time.time() - self.start_time if self.start_time else 0
        self.render()
        
        return True
    
    def render(self):
        """Vẽ toàn bộ giao diện"""
        self.screen.fill(self.COLORS['background'])
        
        self.draw_header()
        self.draw_grid()
        self.draw_sidebar()
        self.draw_buttons()
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def show_completion_message(self):
        """Hiển thị thông báo hoàn thành"""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Khung thông báo
        box_width, box_height = 500, 300
        box_x = (self.WINDOW_WIDTH - box_width) // 2
        box_y = (self.WINDOW_HEIGHT - box_height) // 2
        
        pygame.draw.rect(self.screen, self.COLORS['info_bg'],
                        (box_x, box_y, box_width, box_height), border_radius=15)
        
        y = box_y + 30
        
        # Tiêu đề
        title = self.font_large.render("COMPLETED!", True, self.COLORS['success'])
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, y))
        self.screen.blit(title, title_rect)
        
        y += 60
        
        # Kết quả
        results = [
            f"Found: {len(self.found_words)}/{len(self.grid.words)} words",
            f"Time: {self.elapsed_time:.3f} seconds"
        ]
        
        for result in results:
            text = self.font_medium.render(result, True, self.COLORS['text'])
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 40
        
        # Hướng dẫn
        hint = self.font_small.render("Press ESC to exit", True, self.COLORS['text'])
        hint_rect = hint.get_rect(center=(self.WINDOW_WIDTH // 2, box_y + box_height - 30))
        self.screen.blit(hint, hint_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Chạy GUI"""
        self.render()
        
        waiting_for_start = True
        
        while self.is_running:
            if waiting_for_start:
                self.render()
                result = self.handle_events()
                
                if result == False:
                    break
                
                # Kiểm tra xem đã nhấn Start chưa
                if self.start_time is not None:
                    waiting_for_start = False
                    result = self.solve_step_by_step()
                    
                    if result:
                        self.show_completion_message()
                        
                        # Đợi người dùng thoát
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    waiting = False
                                    self.is_running = False
                            
                            self.clock.tick(30)
            else:
                if not self.handle_events():
                    break
            
            self.clock.tick(60)
        
        pygame.quit()

def run_gui(grid, solver):
    """Hàm chạy GUI"""
    gui = WordSearchGUI(grid, solver)
    gui.run()
