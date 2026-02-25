"""
Chạy Word Search với giao diện pygame
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from grid import Grid
from word_search_dfs import WordSearchDFS
from gui_pygame import run_gui

def main():
    """Hàm main"""
    print("\n" + "="*70)
    print(" "*20 + "WORD SEARCH SOLVER - GUI")
    print("="*70)
    print("\nSelect test case:")
    print("1. Easy (8x8)")
    print("2. Medium (10x10)")
    print("3. Hard (12x12)")
    print("4. Load from file")
    print("0. Exit")
    print("="*70)
    
    choice = input("\nEnter your choice: ")
    
    filepath = None
    
    if choice == '1':
        filepath = os.path.join(os.path.dirname(__file__), 'input', 'easy.txt')
    elif choice == '2':
        filepath = os.path.join(os.path.dirname(__file__), 'input', 'medium.txt')
    elif choice == '3':
        filepath = os.path.join(os.path.dirname(__file__), 'input', 'hard.txt')
    elif choice == '4':
        filepath = input("Enter file path: ")
    elif choice == '0':
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")
        return
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    # Load grid
    print(f"\nLoading: {filepath}")
    grid = Grid()
    grid.load_from_file(filepath)
    
    print(f"Loaded grid: {grid.size}x{grid.size}")
    print(f"Words to find: {len(grid.words)}")
    
    # Tạo solver
    solver = WordSearchDFS(grid)
    
    print("\nStarting GUI...")
    print("\n" + "="*70)
    print("CONTROLS:")
    print("="*70)
    print("• Click 'START' to begin solving")
    print("• Click 'PAUSE' or press SPACE to pause")
    print("• Click 'NEXT' or press RIGHT ARROW for next step")
    print("• Click 'AUTO' or press A for auto play")
    print("• Press ESC to exit")
    print("="*70)
    
    input("\nPress Enter to open GUI...")
    
    # Chạy GUI
    run_gui(grid, solver)
    
    print("\nGUI closed. Goodbye!")

if __name__ == "__main__":
    main()
