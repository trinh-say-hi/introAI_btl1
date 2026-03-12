import os
try:
    from .board import Cage, Board
    from .solver import AStarSolver
except ImportError:
    from board import Cage, Board
    from solver import AStarSolver

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

def read_file(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        n_size = int(lines[0].split()[0])

        initial_board = []
        for i in range(1, n_size + 1):
            row = [int(x) for x in lines[i].split()]
            initial_board.append(row)
        
        num_cages_idx = n_size + 1
        num_cages = int(lines[num_cages_idx])
        cages = []

        for i in range(num_cages_idx + 1, num_cages_idx + 1 + num_cages):
            parts = lines[i].split()
            target_sum = int(parts[0])
            cells = [tuple(map(int, c.split(','))) for c in parts[1:]]
            cages.append(Cage(target_sum, cells))

    return initial_board, cages, n_size

def save_to_file(file_path, board, duration, nodes, memory):
    with open(file_path, "w") as f:
        for row in board:
            f.write(" ".join(map(str, row)) + "\n")

        f.write(f"\n--- Performance Metrics ---")
        f.write(f"\nDuration: {duration:.4f}s")
        f.write(f"\nNodes Expanded: {nodes}")
        f.write(f"\nMemory Usage: {memory / 1024:.2f} KB\n")

if __name__ == "__main__":
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    if not os.path.exists(INPUT_FOLDER):
        print(f"Lỗi: Không tìm thấy thư mục {INPUT_FOLDER}")
    else:
        for file_name in os.listdir(INPUT_FOLDER):
            if file_name.endswith(".txt"):
                input_path = os.path.join(INPUT_FOLDER, file_name)
                output_path = os.path.join(OUTPUT_FOLDER, f"output_astar_{file_name}")

                print(f"--- A* Processing: {file_name} ---")
                board, cages, size = read_file(input_path)

                solver = AStarSolver(board, cages)
                board, duration, nodes, memory = solver.solve()

                if board:
                    print(f"Solved successfully in {duration:.4f}s")
                    save_to_file(output_path, board, duration, nodes, memory)
                else:
                    print(f"No solution found for {file_name}")