"""
Chương trình chính để chạy Word Search Solver
"""
import os
import sys
import io

# Thiết lập encoding UTF-8 cho console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from grid import Grid
from word_search_dfs import WordSearchDFS

def clear_screen():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """In menu chính"""
    print("\n" + "="*60)
    print(" "*15 + "WORD SEARCH SOLVER - DFS")
    print("="*60)
    print("1. Chạy test case có sẵn (Easy)")
    print("2. Chạy test case có sẵn (Medium)")
    print("3. Chạy test case có sẵn (Hard)")
    print("4. Tạo lưới ngẫu nhiên")
    print("5. Tải lưới từ file")
    print("6. So sánh hiệu năng các test case")
    print("0. Thoát")
    print("="*60)

def run_test_case(filename, step_by_step=False, verbose=True):
    """Chạy một test case"""
    print(f"\n📂 Đang tải: {filename}")
    
    grid = Grid()
    grid.load_from_file(filename)
    
    print(f"✅ Đã tải lưới {grid.size}x{grid.size}")
    print(f"🔤 Số từ cần tìm: {len(grid.words)}")
    
    grid.display()
    
    if not step_by_step:
        choice = input("\nBạn có muốn xem từng bước không? (y/n): ").lower()
        step_by_step = (choice == 'y')
    
    solver = WordSearchDFS(grid)
    result = solver.solve(verbose=verbose, step_by_step=step_by_step)
    
    solver.visualize_result()
    
    return result

def create_random_grid():
    """Tạo lưới ngẫu nhiên"""
    print("\n" + "="*60)
    print("TẠO LƯỚI NGẪU NHIÊN")
    print("="*60)
    
    try:
        size = int(input("Nhập kích thước lưới (5-20): "))
        if size < 5 or size > 20:
            print("❌ Kích thước phải từ 5 đến 20")
            return
        
        words_input = input("Nhập các từ cần tìm (cách nhau bởi dấu phẩy): ")
        words = [w.strip() for w in words_input.split(',')]
        
        if not words:
            print("❌ Phải có ít nhất 1 từ")
            return
        
        grid = Grid(size)
        grid.add_words(words)
        grid.fill_random_letters()
        
        print("\n✅ Đã tạo lưới thành công!")
        grid.display()
        
        save_choice = input("\nBạn có muốn lưu lưới này không? (y/n): ").lower()
        if save_choice == 'y':
            filename = input("Nhập tên file (vd: my_grid.txt): ")
            filepath = os.path.join(os.path.dirname(__file__), 'input', filename)
            grid.save_to_file(filepath)
        
        solve_choice = input("\nBạn có muốn giải lưới này không? (y/n): ").lower()
        if solve_choice == 'y':
            step_choice = input("Xem từng bước? (y/n): ").lower()
            step_by_step = (step_choice == 'y')
            
            solver = WordSearchDFS(grid)
            result = solver.solve(verbose=True, step_by_step=step_by_step)
            solver.visualize_result()
        
    except ValueError:
        print("❌ Giá trị không hợp lệ")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def load_from_file():
    """Tải lưới từ file"""
    print("\n" + "="*60)
    print("TẢI LƯỚI TỪ FILE")
    print("="*60)
    
    filename = input("Nhập đường dẫn file: ")
    
    if not os.path.exists(filename):
        print(f"❌ File không tồn tại: {filename}")
        return
    
    run_test_case(filename)

def benchmark_all():
    """So sánh hiệu năng các test case"""
    print("\n" + "="*60)
    print("SO SÁNH HIỆU NĂNG CÁC TEST CASE")
    print("="*60)
    
    test_cases = [
        ('Easy', os.path.join(os.path.dirname(__file__), 'input', 'easy.txt')),
        ('Medium', os.path.join(os.path.dirname(__file__), 'input', 'medium.txt')),
        ('Hard', os.path.join(os.path.dirname(__file__), 'input', 'hard.txt'))
    ]
    
    results = []
    
    for name, filepath in test_cases:
        if not os.path.exists(filepath):
            print(f"❌ Không tìm thấy file: {filepath}")
            continue
        
        print(f"\n{'─'*60}")
        print(f"Đang chạy: {name}")
        print(f"{'─'*60}")
        
        grid = Grid()
        grid.load_from_file(filepath)
        
        solver = WordSearchDFS(grid)
        result = solver.solve(verbose=False, step_by_step=False)
        
        results.append({
            'name': name,
            'size': f"{grid.size}x{grid.size}",
            'words': result['total_words'],
            'found': result['found_count'],
            'time': result['time'],
            'memory': result['memory'],
            'nodes': result['nodes_explored']
        })
    
    print("\n" + "="*60)
    print("BẢNG SO SÁNH KẾT QUẢ")
    print("="*60)
    print(f"{'Test':<10} {'Kích thước':<12} {'Từ':<8} {'Tìm thấy':<10} {'Thời gian (s)':<15} {'Bộ nhớ (MB)':<15} {'Nodes':<10}")
    print("─"*90)
    
    for r in results:
        print(f"{r['name']:<10} {r['size']:<12} {r['words']:<8} {r['found']:<10} {r['time']:<15.6f} {r['memory']:<15.4f} {r['nodes']:<10}")
    
    print("="*60)

def main():
    """Hàm main"""
    while True:
        print_menu()
        choice = input("\nNhập lựa chọn của bạn: ")
        
        if choice == '0':
            print("\n👋 Tạm biệt!")
            break
        elif choice == '1':
            filepath = os.path.join(os.path.dirname(__file__), 'input', 'easy.txt')
            run_test_case(filepath)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '2':
            filepath = os.path.join(os.path.dirname(__file__), 'input', 'medium.txt')
            run_test_case(filepath)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '3':
            filepath = os.path.join(os.path.dirname(__file__), 'input', 'hard.txt')
            run_test_case(filepath)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '4':
            create_random_grid()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '5':
            load_from_file()
            input("\nNhấn Enter để tiếp tục...")
        elif choice == '6':
            benchmark_all()
            input("\nNhấn Enter để tiếp tục...")
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
