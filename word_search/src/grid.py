"""
Module quản lý lưới Word Search
"""
import random
import string

class Grid:
    def __init__(self, size=10):
        """
        Khởi tạo lưới Word Search
        Args:
            size: kích thước lưới (size x size)
        """
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.words = []
        self.word_positions = {}  # Lưu vị trí các từ đã tìm thấy
        
    def create_empty_grid(self):
        """Tạo lưới trống"""
        self.grid = [['' for _ in range(self.size)] for _ in range(self.size)]
        
    def fill_random_letters(self):
        """Điền các ký tự ngẫu nhiên vào ô trống"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == '':
                    self.grid[i][j] = random.choice(string.ascii_uppercase)
    
    def place_word(self, word, row, col, direction):
        """
        Đặt từ vào lưới
        Args:
            word: từ cần đặt
            row, col: vị trí bắt đầu
            direction: hướng đi (0-7)
                0: ngang phải, 1: dọc xuống, 2: chéo phải xuống,
                3: chéo trái xuống, 4: ngang trái, 5: dọc lên,
                6: chéo trái lên, 7: chéo phải lên
        """
        directions = [
            (0, 1),   # ngang phải
            (1, 0),   # dọc xuống
            (1, 1),   # chéo phải xuống
            (1, -1),  # chéo trái xuống
            (0, -1),  # ngang trái
            (-1, 0),  # dọc lên
            (-1, -1), # chéo trái lên
            (-1, 1)   # chéo phải lên
        ]
        
        dr, dc = directions[direction]
        word = word.upper()
        
        for i, char in enumerate(word):
            r = row + i * dr
            c = col + i * dc
            if 0 <= r < self.size and 0 <= c < self.size:
                self.grid[r][c] = char
            else:
                return False
        return True
    
    def can_place_word(self, word, row, col, direction):
        """Kiểm tra có thể đặt từ vào vị trí này không"""
        directions = [
            (0, 1), (1, 0), (1, 1), (1, -1),
            (0, -1), (-1, 0), (-1, -1), (-1, 1)
        ]
        
        dr, dc = directions[direction]
        word = word.upper()
        
        for i, char in enumerate(word):
            r = row + i * dr
            c = col + i * dc
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if self.grid[r][c] != '' and self.grid[r][c] != char:
                return False
        return True
    
    def add_words(self, words):
        """Thêm nhiều từ vào lưới"""
        self.words = [w.upper() for w in words]
        
        for word in self.words:
            placed = False
            attempts = 0
            max_attempts = 100
            
            while not placed and attempts < max_attempts:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
                direction = random.randint(0, 7)
                
                if self.can_place_word(word, row, col, direction):
                    self.place_word(word, row, col, direction)
                    placed = True
                attempts += 1
            
            if not placed:
                print(f"Không thể đặt từ '{word}' sau {max_attempts} lần thử")
    
    def load_from_file(self, filename):
        """Đọc lưới từ file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            self.size = int(lines[0].strip())
            self.grid = []
            
            for i in range(1, self.size + 1):
                row = lines[i].strip().split()
                self.grid.append([c.upper() for c in row])
            
            words_line = lines[self.size + 1].strip()
            self.words = [w.upper() for w in words_line.split(',')]
            
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
    
    def save_to_file(self, filename):
        """Lưu lưới vào file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{self.size}\n")
                for row in self.grid:
                    f.write(' '.join(row) + '\n')
                f.write(','.join(self.words) + '\n')
            print(f"Đã lưu lưới vào {filename}")
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")
    
    def display(self, highlight_positions=None):
        """
        Hiển thị lưới
        Args:
            highlight_positions: list các vị trí (row, col) cần highlight
        """
        print("\n" + "=" * (self.size * 4))
        for i in range(self.size):
            row_str = ""
            for j in range(self.size):
                if highlight_positions and (i, j) in highlight_positions:
                    row_str += f"[{self.grid[i][j]}]"
                else:
                    row_str += f" {self.grid[i][j]} "
            print(row_str)
        print("=" * (self.size * 4))
        print(f"Các từ cần tìm: {', '.join(self.words)}")
        print()

    def get_cell(self, row, col):
        """Lấy ký tự tại vị trí (row, col)"""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None
