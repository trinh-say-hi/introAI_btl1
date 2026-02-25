"""
Module visualize kết quả đẹp hơn với colors
"""
import os

class Visualizer:
    """Class để visualize Word Search với màu sắc"""
    
    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    
    @staticmethod
    def clear_screen():
        """Xóa màn hình"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(text):
        """In header đẹp"""
        width = 70
        print("\n" + Visualizer.CYAN + "=" * width + Visualizer.RESET)
        print(Visualizer.BOLD + Visualizer.YELLOW + text.center(width) + Visualizer.RESET)
        print(Visualizer.CYAN + "=" * width + Visualizer.RESET)
    
    @staticmethod
    def print_grid(grid, highlight_positions=None, word_paths=None):
        """
        In lưới với màu sắc
        Args:
            grid: đối tượng Grid
            highlight_positions: set các vị trí cần highlight
            word_paths: dict {word: path} để hiển thị nhiều màu
        """
        size = grid.size
        
        # Màu cho mỗi từ
        colors = [
            Visualizer.BG_RED, Visualizer.BG_GREEN, Visualizer.BG_YELLOW,
            Visualizer.BG_BLUE, Visualizer.BG_MAGENTA, Visualizer.BG_CYAN
        ]
        
        # Map vị trí -> màu
        position_colors = {}
        if word_paths:
            for idx, (word, info) in enumerate(word_paths.items()):
                color = colors[idx % len(colors)]
                for pos in info['path']:
                    position_colors[pos] = color
        
        print("\n" + Visualizer.CYAN + "┌" + "─" * (size * 4 - 1) + "┐" + Visualizer.RESET)
        
        for i in range(size):
            row_str = Visualizer.CYAN + "│" + Visualizer.RESET
            for j in range(size):
                char = grid.grid[i][j]
                
                if (i, j) in position_colors:
                    # Highlight với màu của từ
                    color = position_colors[(i, j)]
                    row_str += color + Visualizer.BOLD + f" {char} " + Visualizer.RESET
                elif highlight_positions and (i, j) in highlight_positions:
                    # Highlight đơn giản
                    row_str += Visualizer.BG_GREEN + Visualizer.BOLD + f" {char} " + Visualizer.RESET
                else:
                    # Ký tự bình thường
                    row_str += f" {char} "
                
                if j < size - 1:
                    row_str += " "
            
            row_str += Visualizer.CYAN + "│" + Visualizer.RESET
            print(row_str)
        
        print(Visualizer.CYAN + "└" + "─" * (size * 4 - 1) + "┘" + Visualizer.RESET)
    
    @staticmethod
    def print_word_list(words, found_words=None):
        """In danh sách từ với status"""
        print("\n" + Visualizer.BOLD + "Các từ cần tìm:" + Visualizer.RESET)
        
        for word in words:
            if found_words and word in found_words:
                print(f"  {Visualizer.GREEN}✅ {word}{Visualizer.RESET}")
            else:
                print(f"  {Visualizer.RED}❌ {word}{Visualizer.RESET}")
    
    @staticmethod
    def print_result(result):
        """In kết quả đẹp"""
        print("\n" + Visualizer.BOLD + Visualizer.GREEN + "KẾT QUẢ" + Visualizer.RESET)
        print(Visualizer.CYAN + "─" * 70 + Visualizer.RESET)
        
        print(f"{Visualizer.YELLOW}✅ Tìm thấy:{Visualizer.RESET} "
              f"{Visualizer.GREEN}{result['found_count']}{Visualizer.RESET}/"
              f"{result['total_words']} từ")
        
        print(f"{Visualizer.YELLOW}⏱️  Thời gian:{Visualizer.RESET} "
              f"{Visualizer.CYAN}{result['time']:.6f}{Visualizer.RESET} giây")
        
        print(f"{Visualizer.YELLOW}💾 Bộ nhớ:{Visualizer.RESET} "
              f"{Visualizer.CYAN}{result['memory']:.4f}{Visualizer.RESET} MB")
        
        print(f"{Visualizer.YELLOW}🔢 Nodes:{Visualizer.RESET} "
              f"{Visualizer.CYAN}{result['nodes_explored']}{Visualizer.RESET}")
        
        if result['time'] > 0:
            speed = result['nodes_explored'] / result['time']
            print(f"{Visualizer.YELLOW}⚡ Tốc độ:{Visualizer.RESET} "
                  f"{Visualizer.CYAN}{speed:.2f}{Visualizer.RESET} nodes/giây")
    
    @staticmethod
    def print_found_words(found_words):
        """In danh sách từ đã tìm thấy"""
        if not found_words:
            print(f"\n{Visualizer.RED}Không tìm thấy từ nào!{Visualizer.RESET}")
            return
        
        print("\n" + Visualizer.BOLD + "Chi tiết các từ tìm thấy:" + Visualizer.RESET)
        print(Visualizer.CYAN + "─" * 70 + Visualizer.RESET)
        
        for word, info in found_words.items():
            print(f"{Visualizer.GREEN}✅ {Visualizer.BOLD}{word}{Visualizer.RESET}")
            print(f"   Bắt đầu: {Visualizer.YELLOW}{info['start']}{Visualizer.RESET}")
            print(f"   Kết thúc: {Visualizer.YELLOW}{info['end']}{Visualizer.RESET}")
            print(f"   Hướng: {Visualizer.CYAN}{info['direction']}{Visualizer.RESET}")
    
    @staticmethod
    def print_progress(current, total, word=""):
        """In progress bar"""
        percent = int((current / total) * 100)
        filled = int(percent / 2)
        bar = "█" * filled + "░" * (50 - filled)
        
        print(f"\r{Visualizer.CYAN}[{bar}]{Visualizer.RESET} "
              f"{percent}% {Visualizer.YELLOW}{word}{Visualizer.RESET}", 
              end='', flush=True)
        
        if current == total:
            print()
    
    @staticmethod
    def print_comparison_table(results):
        """In bảng so sánh các kết quả"""
        print("\n" + Visualizer.BOLD + "BẢNG SO SÁNH KẾT QUẢ" + Visualizer.RESET)
        print(Visualizer.CYAN + "=" * 90 + Visualizer.RESET)
        
        # Header
        header = f"{'Test':<12} {'Size':<10} {'Words':<10} {'Found':<10} {'Time(s)':<12} {'Memory(MB)':<12} {'Nodes':<10}"
        print(Visualizer.BOLD + header + Visualizer.RESET)
        print(Visualizer.CYAN + "─" * 90 + Visualizer.RESET)
        
        # Rows
        for r in results:
            found_color = Visualizer.GREEN if r['found_words'] == r['total_words'] else Visualizer.YELLOW
            
            row = (f"{r['test_name']:<12} "
                   f"{r['grid_size']}x{r['grid_size']:<8} "
                   f"{r['total_words']:<10} "
                   f"{found_color}{r['found_words']}/{r['total_words']}{Visualizer.RESET:<10} "
                   f"{r['time_seconds']:<12.6f} "
                   f"{r['memory_mb']:<12.4f} "
                   f"{r['nodes_explored']:<10}")
            print(row)
        
        print(Visualizer.CYAN + "=" * 90 + Visualizer.RESET)
    
    @staticmethod
    def print_error(message):
        """In thông báo lỗi"""
        print(f"\n{Visualizer.RED}❌ LỖI: {message}{Visualizer.RESET}")
    
    @staticmethod
    def print_success(message):
        """In thông báo thành công"""
        print(f"\n{Visualizer.GREEN}✅ {message}{Visualizer.RESET}")
    
    @staticmethod
    def print_info(message):
        """In thông tin"""
        print(f"{Visualizer.CYAN}ℹ️  {message}{Visualizer.RESET}")
    
    @staticmethod
    def print_warning(message):
        """In cảnh báo"""
        print(f"{Visualizer.YELLOW}⚠️  {message}{Visualizer.RESET}")
