# BÁO CÁO BÀI TẬP LỚN 1
## ĐỀ TÀI: GIẢI BÀI TOÁN WORD SEARCH BẰNG THUẬT TOÁN TÌM KIẾM

---

### THÔNG TIN NHÓM

**Tên nhóm:** [Nhập tên nhóm]

**Danh sách thành viên:**
| STT | Họ và tên | MSSV | Email | Công việc |
|-----|-----------|------|-------|-----------|
| 1   | [Tên]     | [MSSV] | [Email] | [Vai trò] |
| 2   | [Tên]     | [MSSV] | [Email] | [Vai trò] |
| 3   | [Tên]     | [MSSV] | [Email] | [Vai trò] |

**Giảng viên hướng dẫn:** [Tên giảng viên]

**Học kỳ:** 2 (2025-2026)

**Ngày nộp:** 24/03/2026

---

## MỤC LỤC

1. [Giới thiệu](#1-giới-thiệu)
2. [Bài toán Word Search](#2-bài-toán-word-search)
3. [Thuật toán DFS](#3-thuật-toán-dfs)
4. [Hiện thực](#4-hiện-thực)
5. [Kết quả thử nghiệm](#5-kết-quả-thử-nghiệm)
6. [Phân tích và đánh giá](#6-phân-tích-và-đánh-giá)
7. [Kết luận](#7-kết-luận)
8. [Tài liệu tham khảo](#8-tài-liệu-tham-khảo)

---

## 1. GIỚI THIỆU

### 1.1. Đặt vấn đề

[Mô tả tại sao chọn bài toán này, ý nghĩa của bài toán]

### 1.2. Mục tiêu

- Hiện thực thuật toán DFS (Depth-First Search) để giải bài toán Word Search
- Đo đạc và đánh giá hiệu năng thuật toán
- Phân tích độ phức tạp thời gian và không gian

### 1.3. Phạm vi

- Ngôn ngữ: Python 3
- Thuật toán: DFS
- Test cases: 3 mức độ (Easy, Medium, Hard)

---

## 2. BÀI TOÁN WORD SEARCH

### 2.1. Mô tả bài toán

Word Search (Tìm từ trong lưới) là một trò chơi puzzle trong đó:

**Input:**
- Lưới chữ cái kích thước `n × n`
- Danh sách `k` từ cần tìm

**Output:**
- Vị trí và hướng của mỗi từ trong lưới (nếu có)

**Ràng buộc:**
- Các từ có thể nằm theo 8 hướng:
  - Ngang: trái, phải
  - Dọc: lên, xuống
  - Chéo: 4 hướng

### 2.2. Ví dụ

```
Lưới 5×5:
H E L L O
W O R L D
P Y T H O
N J A V A
X Y Z A B

Từ cần tìm: HELLO, WORLD, PYTHON
```

**Kết quả:**
- HELLO: (0,0) → (0,4) (ngang phải)
- WORLD: (1,1) → (1,4) (ngang phải)  
- PYTHON: (2,0) → (2,4) (ngang phải)

### 2.3. Độ phức tạp bài toán

- **Không gian trạng thái:** [Phân tích]
- **Branching factor:** [Phân tích]
- **Độ sâu tối đa:** [Phân tích]

---

## 3. THUẬT TOÁN DFS

### 3.1. Giới thiệu DFS

DFS (Depth-First Search) là thuật toán tìm kiếm mù (blind search) thuộc nhóm uninformed search.

**Đặc điểm:**
- Duyệt theo chiều sâu
- Sử dụng stack (hoặc đệ quy)
- Không đảm bảo tìm được đường đi ngắn nhất

### 3.2. Áp dụng DFS cho Word Search

**Ý tưởng:**

1. Quét toàn bộ lưới để tìm ký tự đầu tiên của từ cần tìm
2. Từ mỗi vị trí tìm thấy, thử 8 hướng
3. Với mỗi hướng, sử dụng DFS đệ quy để tìm các ký tự tiếp theo
4. Nếu tìm đủ tất cả ký tự → Thành công
5. Nếu không → Backtrack và thử hướng khác

### 3.3. Pseudocode

```python
function SOLVE_WORD_SEARCH(grid, words):
    found_words = {}
    
    for each word in words:
        result = FIND_WORD(grid, word)
        if result is not None:
            found_words[word] = result
    
    return found_words

function FIND_WORD(grid, word):
    for i from 0 to n-1:
        for j from 0 to n-1:
            if grid[i][j] == word[0]:
                for each direction in 8_DIRECTIONS:
                    path = DFS_SEARCH(word, i, j, direction, 0, [])
                    if path is not None:
                        return path
    return None

function DFS_SEARCH(word, row, col, direction, index, path):
    if index == length(word):
        return path
    
    new_row = row + direction.dr
    new_col = col + direction.dc
    
    if not is_valid(new_row, new_col):
        return None
    
    if grid[new_row][new_col] != word[index]:
        return None
    
    new_path = path + [(new_row, new_col)]
    return DFS_SEARCH(word, new_row, new_col, direction, index+1, new_path)
```

### 3.4. Phân tích độ phức tạp

**Độ phức tạp thời gian:**
- **Trường hợp xấu nhất:** O(N × M × 8 × L)
  - N × M: kích thước lưới
  - 8: số hướng cần thử
  - L: độ dài trung bình của từ

**Độ phức tạp không gian:**
- **Stack đệ quy:** O(L)
  - L: độ dài từ dài nhất

---

## 4. HIỆN THỰC

### 4.1. Ngôn ngữ và công cụ

- **Ngôn ngữ:** Python 3.11
- **Thư viện:** 
  - `time`: Đo thời gian
  - `tracemalloc`: Đo bộ nhớ
  - `collections`: Cấu trúc dữ liệu

### 4.2. Cấu trúc chương trình

```
word_search/
├── src/
│   ├── grid.py               # Class quản lý lưới
│   └── word_search_dfs.py    # Thuật toán DFS
├── input/                    # Test cases
├── main.py                   # Chương trình chính
└── benchmark.py              # Đo hiệu năng
```

### 4.3. Các module chính

#### 4.3.1. Grid (grid.py)

**Chức năng:**
- Tạo và quản lý lưới Word Search
- Đọc/ghi file input
- Hiển thị lưới với highlight

**Các phương thức chính:**
```python
class Grid:
    def __init__(self, size)
    def load_from_file(self, filename)
    def display(self, highlight_positions)
    def get_cell(self, row, col)
```

#### 4.3.2. WordSearchDFS (word_search_dfs.py)

**Chức năng:**
- Hiện thực thuật toán DFS
- Tìm kiếm từ trong lưới
- Đo đạc hiệu năng

**Các phương thức chính:**
```python
class WordSearchDFS:
    def __init__(self, grid)
    def dfs_search_word(self, word, row, col, direction, index, path)
    def find_word(self, word, verbose)
    def solve(self, verbose, step_by_step)
```

### 4.4. Các tính năng

✅ Tìm kiếm theo 8 hướng  
✅ Hiển thị step-by-step  
✅ Visualize kết quả  
✅ Đo thời gian và bộ nhớ  
✅ Benchmark tự động  

---

## 5. KẾT QUẢ THỬ NGHIỆM

### 5.1. Môi trường thử nghiệm

- **CPU:** [Nhập thông tin CPU]
- **RAM:** [Nhập dung lượng RAM]
- **OS:** Windows 10/11 / Linux / macOS
- **Python:** 3.11.x

### 5.2. Test cases

#### Test Case 1: Easy
- **Kích thước:** 8×8 (64 ô)
- **Số từ:** 10 từ
- **Tổng ký tự:** 39 ký tự

#### Test Case 2: Medium
- **Kích thước:** 10×10 (100 ô)
- **Số từ:** 16 từ
- **Tổng ký tự:** 85 ký tự

#### Test Case 3: Hard
- **Kích thước:** 12×12 (144 ô)
- **Số từ:** 11 từ
- **Tổng ký tự:** 78 ký tự

### 5.3. Kết quả thực nghiệm

#### Bảng 1: So sánh thời gian thực thi

| Test Case | Kích thước | Số từ | Thời gian (s) | Nodes đã duyệt |
|-----------|------------|-------|---------------|----------------|
| Easy      | 8×8        | 10    | 0.000838      | 135            |
| Medium    | 10×10      | 16    | 0.002735      | 349            |
| Hard      | 12×12      | 11    | 0.002254      | 403            |

#### Bảng 2: So sánh bộ nhớ sử dụng

| Test Case | Bộ nhớ (MB) | Bộ nhớ peak (MB) |
|-----------|-------------|------------------|
| Easy      | 0.0034      | 0.0034           |
| Medium    | 0.0064      | 0.0064           |
| Hard      | 0.0024      | 0.0024           |

#### Bảng 3: Hiệu quả tìm kiếm

| Test Case | Tìm thấy | Tỷ lệ thành công | Tốc độ (nodes/s) |
|-----------|----------|------------------|------------------|
| Easy      | 10/10    | 100.0%           | 161,089          |
| Medium    | 16/16    | 100.0%           | 127,587          |
| Hard      | 10/11    | 90.9%            | 178,773          |

### 5.4. Biểu đồ

[Chèn biểu đồ thời gian, bộ nhớ, hiệu quả]

---

## 6. PHÂN TÍCH VÀ ĐÁNH GIÁ

### 6.1. Phân tích kết quả

#### 6.1.1. Thời gian thực thi

[Phân tích xu hướng thời gian tăng theo kích thước lưới]

**Nhận xét:**
- Thời gian tăng tuyến tính với kích thước lưới
- DFS rất nhanh với lưới nhỏ (< 3ms)
- Tốc độ trung bình: ~155,000 nodes/giây

#### 6.1.2. Bộ nhớ sử dụng

[Phân tích mức độ tiêu tốn bộ nhớ]

**Nhận xét:**
- Bộ nhớ rất thấp (< 0.01 MB)
- Không tăng nhiều theo kích thước lưới
- Phù hợp với phân tích lý thuyết O(L)

#### 6.1.3. Hiệu quả tìm kiếm

[Phân tích tỷ lệ tìm thấy từ]

**Nhận xét:**
- Tỷ lệ thành công cao (90-100%)
- Có thể cải thiện bằng cách xử lý edge cases tốt hơn

### 6.2. Ưu điểm của DFS

✅ **Đơn giản:** Dễ hiện thực  
✅ **Hiệu quả:** Nhanh với lưới vừa và nhỏ  
✅ **Tiết kiệm bộ nhớ:** Chỉ cần O(L) không gian  
✅ **Tìm kiếm theo hướng:** Phù hợp với Word Search  

### 6.3. Nhược điểm của DFS

❌ **Không tối ưu:** Không đảm bảo tìm được lời giải tốt nhất  
❌ **Có thể bị mắc kẹt:** Với lưới phức tạp  
❌ **Phụ thuộc thứ tự:** Kết quả phụ thuộc vào thứ tự duyệt  

### 6.4. So sánh với các thuật toán khác

| Thuật toán | Thời gian | Bộ nhớ | Độ phức tạp | Ưu điểm |
|------------|-----------|--------|-------------|---------|
| DFS        | Nhanh     | Thấp   | O(N×M×8×L)  | Đơn giản, hiệu quả |
| BFS        | Trung bình| Cao    | O(N×M×8×L)  | Tìm đường ngắn nhất |
| A*         | Rất nhanh | Cao    | O(b^d)      | Tối ưu với heuristic tốt |

### 6.5. Đề xuất cải tiến

1. **Tối ưu hóa:**
   - Sử dụng Trie để lưu trữ từ điển
   - Pruning các nhánh không triển vọng

2. **Mở rộng:**
   - Hỗ trợ từ có thể uốn cong
   - Tìm nhiều từ cùng lúc

3. **Song song hóa:**
   - Tìm kiếm nhiều từ song song
   - Sử dụng multi-threading

---

## 7. KẾT LUẬN

### 7.1. Tổng kết

[Tóm tắt những gì đã làm được]

### 7.2. Bài học kinh nghiệm

[Những kinh nghiệm rút ra được]

### 7.3. Hướng phát triển

[Hướng phát triển trong tương lai]

---

## 8. TÀI LIỆU THAM KHẢO

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.

2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

3. Tài liệu môn học Trí tuệ nhân tạo, Trường [Tên trường], Học kỳ 2 (2025-2026).

4. Python Documentation: https://docs.python.org/3/

5. Depth-First Search: https://en.wikipedia.org/wiki/Depth-first_search

6. Word Search Puzzle: https://www.puzzle-pipes.com/

---

## PHU LỤC

### A. Source code

[Đính kèm link GitHub hoặc code chính]

### B. Screenshots

[Chèn ảnh chụp màn hình demo]

### C. Video demo

[Link video demo (nếu có)]

### D. Benchmark results

[File JSON kết quả benchmark đầy đủ]

---

**Ngày hoàn thành báo cáo:** [Ngày/Tháng/Năm]

**Chữ ký nhóm trưởng:**

---
