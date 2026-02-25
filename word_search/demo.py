"""
File demo tự động - chạy tất cả test cases
"""
import os
import sys
import io

# Thiết lập encoding UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from grid import Grid
from word_search_dfs import WordSearchDFS
from word_search_bfs import WordSearchBFS

def demo_single_test(test_name, filepath):
    """Demo một test case"""
    print("\n" + "="*70)
    print(f" DEMO: {test_name}")
    print("="*70)
    
    grid = Grid()
    grid.load_from_file(filepath)
    
    print(f"\n📊 Thông tin lưới:")
    print(f"   - Kích thước: {grid.size}x{grid.size}")
    print(f"   - Số từ cần tìm: {len(grid.words)}")
    
    grid.display()
    
    print("\n" + "─"*70)
    print("THUẬT TOÁN DFS")
    print("─"*70)
    
    solver_dfs = WordSearchDFS(grid)
    result_dfs = solver_dfs.solve(verbose=False, step_by_step=False)
    solver_dfs.visualize_result()
    
    return result_dfs

def demo_all():
    """Demo tất cả test cases"""
    print("\n" + "="*70)
    print(" "*20 + "WORD SEARCH SOLVER DEMO")
    print(" "*25 + "Sử dụng thuật toán DFS")
    print("="*70)
    
    test_cases = [
        ('EASY - Lưới 8x8', os.path.join(os.path.dirname(__file__), 'input', 'easy.txt')),
        ('MEDIUM - Lưới 10x10', os.path.join(os.path.dirname(__file__), 'input', 'medium.txt')),
        ('HARD - Lưới 12x12', os.path.join(os.path.dirname(__file__), 'input', 'hard.txt'))
    ]
    
    results = []
    
    for test_name, filepath in test_cases:
        if os.path.exists(filepath):
            result = demo_single_test(test_name, filepath)
            results.append((test_name, result))
            input("\n⏸️  Nhấn Enter để tiếp tục...")
        else:
            print(f"❌ Không tìm thấy file: {filepath}")
    
    print("\n" + "="*70)
    print(" "*25 + "TỔNG KẾT")
    print("="*70)
    
    print(f"\n{'Test Case':<20} {'Tìm thấy':<15} {'Thời gian (s)':<15} {'Bộ nhớ (MB)':<15} {'Nodes':<10}")
    print("─"*85)
    
    for test_name, result in results:
        print(f"{test_name:<20} "
              f"{result['found_count']}/{result['total_words']:<12} "
              f"{result['time']:<15.6f} "
              f"{result['memory']:<15.4f} "
              f"{result['nodes_explored']:<10}")
    
    print("="*70)
    print("\n✅ Demo hoàn tất!")

if __name__ == "__main__":
    demo_all()
