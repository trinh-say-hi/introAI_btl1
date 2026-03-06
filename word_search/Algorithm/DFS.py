"""
Thuật toán DFS (Depth-First Search) để giải Word Search
"""
import time
import tracemalloc

class WordSearchDFS:
    def __init__(self, grid):
        """
        Khởi tạo solver DFS
        Args:
            grid: đối tượng Grid
        """
        self.grid = grid
        self.size = grid.size
        self.found_words = {}
        self.search_path = []  # Lưu đường đi tìm kiếm để visualize
        self.nodes_explored = 0
        
        # 8 hướng: phải, xuống, chéo phải xuống, chéo trái xuống,
        #          trái, lên, chéo trái lên, chéo phải lên
        self.directions = [
            (0, 1),   # ngang phải
            (1, 0),   # dọc xuống
            (1, 1),   # chéo phải xuống
            (1, -1),  # chéo trái xuống
            (0, 1),  # ngang trái
            (-1, 0),  # dọc lên
            (-1, -1), # chéo trái lên
            (-1, 1)   # chéo phải lên
        ]
        
        self.direction_names = [
            "ngang phải", "dọc xuống", "chéo phải xuống", "chéo trái xuống",
            "ngang trái", "dọc lên", "chéo trái lên", "chéo phải lên"
        ]
    
    def is_valid(self, row, col):
        """Kiểm tra vị trí có hợp lệ không"""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def dfs_search_word(self, word, row, col, direction, index, path):
        """
        DFS tìm kiếm từ theo một hướng cụ thể
        Args:
            word: từ cần tìm
            row, col: vị trí hiện tại
            direction: hướng tìm kiếm (dr, dc)
            index: chỉ số ký tự hiện tại trong word
            path: đường đi hiện tại
        Returns:
            path nếu tìm thấy, None nếu không
        """
        self.nodes_explored += 1
        
        if index == len(word):
            return path
        
        dr, dc = direction
        new_row = row + dr
        new_col = col + dc
        
        if not self.is_valid(new_row, new_col):
            return None
        
        if self.grid.get_cell(new_row, new_col) != word[index]:
            return None
        
        new_path = path + [(new_row, new_col)]
        return self.dfs_search_word(word, new_row, new_col, direction, index + 1, new_path)
    
    def get_neighbor_positions(self, row, col):
        """
        Lấy 8 ô lân cận của vị trí (row, col) để visualize
        Returns:
            list các vị trí (row, col) hợp lệ
        """
        neighbors = []
        for dr, dc in self.directions:
            new_row = row + dr
            new_col = col + dc
            if self.is_valid(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors
    
    def find_word(self, word, verbose=False):
        """
        Tìm một từ trong lưới sử dụng DFS
        Args:
            word: từ cần tìm
            verbose: có in thông tin chi tiết không
        Returns:
            dict chứa thông tin về từ tìm thấy hoặc None
        """
        word = word.upper()
        if verbose:
            print(f"\n🔍 Đang tìm từ: '{word}'")
        
        for i in range(self.size):
            for j in range(self.size):
                if self.grid.get_cell(i, j) == word[0]:
                    if verbose:
                        print(f"  Tìm thấy ký tự đầu '{word[0]}' tại ({i}, {j})")
                    
                    for dir_idx, direction in enumerate(self.directions):
                        path = [(i, j)]
                        result = self.dfs_search_word(word, i, j, direction, 1, path)
                        
                        if result:
                            if verbose:
                                print(f"  ✅ Tìm thấy từ theo hướng {self.direction_names[dir_idx]}")
                                print(f"  Đường đi: {result}")
                            
                            return {
                                'word': word,
                                'start': (i, j),
                                'end': result[-1],
                                'direction': self.direction_names[dir_idx],
                                'path': result
                            }
        
        if verbose:
            print(f"  ❌ Không tìm thấy từ '{word}'")
        return None
    
    def solve(self, verbose=False, step_by_step=False):
        """
        Giải toàn bộ Word Search puzzle
        Args:
            verbose: có in thông tin chi tiết không
            step_by_step: có hiển thị từng bước không
        Returns:
            dict chứa kết quả tìm kiếm
        """
        print("\n" + "="*60)
        print("BẮT ĐẦU GIẢI WORD SEARCH BẰNG THUẬT TOÁN DFS")
        print("="*60)
        
        self.found_words = {}
        self.nodes_explored = 0
        
        tracemalloc.start()
        start_time = time.time()
        
        for word in self.grid.words:
            if step_by_step:
                print(f"\n{'─'*60}")
                self.grid.display()
            
            result = self.find_word(word, verbose=verbose or step_by_step)
            
            if result:
                self.found_words[word] = result
                if step_by_step:
                    print(f"\n✅ Tìm thấy: '{word}'")
                    print(f"   Vị trí: {result['start']} → {result['end']}")
                    print(f"   Hướng: {result['direction']}")
                    self.grid.display(highlight_positions=result['path'])
                    input("   Nhấn Enter để tiếp tục...")
        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        elapsed_time = end_time - start_time
        memory_used = peak / 1024 / 1024
        
        print("\n" + "="*60)
        print("KẾT QUẢ")
        print("="*60)
        print(f"✅ Tìm thấy: {len(self.found_words)}/{len(self.grid.words)} từ")
        print(f"⏱️  Thời gian: {elapsed_time:.6f} giây")
        print(f"💾 Bộ nhớ: {memory_used:.4f} MB")
        print(f"🔢 Số node đã duyệt: {self.nodes_explored}")
        
        if verbose:
            print("\nChi tiết các từ tìm thấy:")
            for word, info in self.found_words.items():
                print(f"  • {word}: {info['start']} → {info['end']} ({info['direction']})")
        
        return {
            'found_words': self.found_words,
            'total_words': len(self.grid.words),
            'found_count': len(self.found_words),
            'time': elapsed_time,
            'memory': memory_used,
            'nodes_explored': self.nodes_explored
        }
    
    def visualize_result(self):
        """Hiển thị kết quả với các từ được highlight"""
        print("\n" + "="*60)
        print("LƯỚI VỚI CÁC TỪ TÌM THẤY")
        print("="*60)
        
        all_positions = set()
        for word, info in self.found_words.items():
            all_positions.update(info['path'])
        
        self.grid.display(highlight_positions=all_positions)
        
        print("Danh sách từ tìm thấy:")
        for word, info in self.found_words.items():
            print(f"  ✅ {word}: {info['start']} → {info['end']} ({info['direction']})")
