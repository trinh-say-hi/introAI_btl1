"""
Module đo lường và so sánh hiệu năng
"""
import os
import sys
import time
import tracemalloc
import json
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from grid import Grid
from word_search_dfs import WordSearchDFS

class Benchmark:
    def __init__(self):
        self.results = []
    
    def run_test(self, test_name, filepath, algorithm='DFS'):
        """
        Chạy một test case và đo lường hiệu năng
        """
        print(f"\n{'='*70}")
        print(f"🧪 Test: {test_name} | Thuật toán: {algorithm}")
        print(f"{'='*70}")
        
        grid = Grid()
        grid.load_from_file(filepath)
        
        print(f"📊 Thông tin:")
        print(f"   - Kích thước lưới: {grid.size}x{grid.size}")
        print(f"   - Số ô: {grid.size * grid.size}")
        print(f"   - Số từ cần tìm: {len(grid.words)}")
        print(f"   - Tổng số ký tự cần tìm: {sum(len(w) for w in grid.words)}")
        
        tracemalloc.start()
        start_time = time.time()
        
        if algorithm == 'DFS':
            solver = WordSearchDFS(grid)
            result = solver.solve(verbose=False, step_by_step=False)
        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        elapsed_time = end_time - start_time
        memory_mb = peak / 1024 / 1024
        
        test_result = {
            'test_name': test_name,
            'algorithm': algorithm,
            'grid_size': grid.size,
            'total_cells': grid.size * grid.size,
            'total_words': len(grid.words),
            'total_chars': sum(len(w) for w in grid.words),
            'found_words': result['found_count'],
            'time_seconds': elapsed_time,
            'memory_mb': memory_mb,
            'nodes_explored': result['nodes_explored'],
            'success_rate': result['found_count'] / len(grid.words) * 100
        }
        
        self.results.append(test_result)
        
        print(f"\n📈 Kết quả:")
        print(f"   ✅ Tìm thấy: {result['found_count']}/{len(grid.words)} từ ({test_result['success_rate']:.1f}%)")
        print(f"   ⏱️  Thời gian: {elapsed_time:.6f} giây")
        print(f"   💾 Bộ nhớ: {memory_mb:.4f} MB")
        print(f"   🔢 Nodes duyệt: {result['nodes_explored']}")
        print(f"   ⚡ Tốc độ: {result['nodes_explored']/elapsed_time:.2f} nodes/giây")
        
        return test_result
    
    def run_all_tests(self):
        """Chạy tất cả test cases"""
        test_cases = [
            ('Easy', os.path.join(os.path.dirname(__file__), 'input', 'easy.txt')),
            ('Medium', os.path.join(os.path.dirname(__file__), 'input', 'medium.txt')),
            ('Hard', os.path.join(os.path.dirname(__file__), 'input', 'hard.txt'))
        ]
        
        print("\n" + "="*70)
        print(" "*20 + "BENCHMARK - WORD SEARCH SOLVER")
        print("="*70)
        
        for test_name, filepath in test_cases:
            if os.path.exists(filepath):
                self.run_test(test_name, filepath, 'DFS')
            else:
                print(f"❌ Không tìm thấy file: {filepath}")
        
        self.print_summary()
        self.save_results()
    
    def print_summary(self):
        """In bảng tổng kết"""
        print("\n" + "="*70)
        print(" "*25 + "BẢNG TỔNG KẾT")
        print("="*70)
        
        print(f"\n{'Test':<10} {'Lưới':<10} {'Từ':<6} {'Tìm thấy':<10} {'Thời gian(s)':<13} {'Bộ nhớ(MB)':<12} {'Nodes':<10}")
        print("─"*85)
        
        for r in self.results:
            print(f"{r['test_name']:<10} "
                  f"{r['grid_size']}x{r['grid_size']:<7} "
                  f"{r['total_words']:<6} "
                  f"{r['found_words']}/{r['total_words']:<7} "
                  f"{r['time_seconds']:<13.6f} "
                  f"{r['memory_mb']:<12.4f} "
                  f"{r['nodes_explored']:<10}")
        
        print("="*70)
        
        if len(self.results) > 0:
            avg_time = sum(r['time_seconds'] for r in self.results) / len(self.results)
            avg_memory = sum(r['memory_mb'] for r in self.results) / len(self.results)
            total_words = sum(r['total_words'] for r in self.results)
            total_found = sum(r['found_words'] for r in self.results)
            
            print(f"\n📊 Thống kê:")
            print(f"   • Tổng số test: {len(self.results)}")
            print(f"   • Tổng số từ: {total_words}")
            print(f"   • Tổng tìm thấy: {total_found} ({total_found/total_words*100:.1f}%)")
            print(f"   • Thời gian trung bình: {avg_time:.6f} giây")
            print(f"   • Bộ nhớ trung bình: {avg_memory:.4f} MB")
    
    def save_results(self):
        """Lưu kết quả ra file JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_results_{timestamp}.json"
        
        output = {
            'timestamp': timestamp,
            'algorithm': 'DFS',
            'results': self.results
        }
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Đã lưu kết quả vào: {filename}")
    
    def generate_report_data(self):
        """Tạo dữ liệu cho báo cáo"""
        print("\n" + "="*70)
        print(" "*20 + "DỮ LIỆU CHO BÁO CÁO")
        print("="*70)
        
        print("\n📋 Bảng 1: So sánh thời gian thực thi")
        print("─"*70)
        print(f"{'Test Case':<15} {'Kích thước':<12} {'Số từ':<10} {'Thời gian (s)':<15}")
        print("─"*70)
        for r in self.results:
            print(f"{r['test_name']:<15} {r['grid_size']}x{r['grid_size']:<10} {r['total_words']:<10} {r['time_seconds']:<15.6f}")
        
        print("\n📋 Bảng 2: So sánh bộ nhớ sử dụng")
        print("─"*70)
        print(f"{'Test Case':<15} {'Bộ nhớ (MB)':<15} {'Nodes đã duyệt':<20}")
        print("─"*70)
        for r in self.results:
            print(f"{r['test_name']:<15} {r['memory_mb']:<15.4f} {r['nodes_explored']:<20}")
        
        print("\n📋 Bảng 3: Hiệu quả tìm kiếm")
        print("─"*70)
        print(f"{'Test Case':<15} {'Tìm thấy':<12} {'Tỷ lệ thành công':<20}")
        print("─"*70)
        for r in self.results:
            print(f"{r['test_name']:<15} {r['found_words']}/{r['total_words']:<9} {r['success_rate']:<20.2f}%")

def main():
    """Hàm main"""
    benchmark = Benchmark()
    benchmark.run_all_tests()
    benchmark.generate_report_data()
    
    print("\n" + "="*70)
    print("✅ Hoàn thành benchmark!")
    print("="*70)

if __name__ == "__main__":
    main()
