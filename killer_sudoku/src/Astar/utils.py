class KillerSudokuUtils:
    @staticmethod
    def is_valid(board, row, col, num, board_obj):
        n = len(board)
        subgrid_size = int(n**0.5)

        for i in range(n):
            if board[row][i] == num or board[i][col] == num:
                return False
            
        start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
        for i in range(subgrid_size):
            for j in range(subgrid_size):
                if board[start_row + i][start_col + j] == num:
                    return False
                
        cage = board_obj.cage_map.get((row, col))
        if not cage:
            return True
        
        current_sum = 0
        empty_count = 0
        for cage_row, cage_col in cage.cells:
            val = board[cage_row][cage_col] if (cage_row, cage_col) != (row, col) else num
            if val == 0:
                empty_count += 1
            else:
                if val == num and (cage_row, cage_col) != (row, col):
                    return False
                current_sum += val
        
        if empty_count == 0:
            return current_sum == cage.target_sum
        
        return current_sum < cage.target_sum