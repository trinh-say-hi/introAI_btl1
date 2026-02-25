# HƯỚNG DẪN SỬ DỤNG - WORD SEARCH SOLVER

## 📋 Giới thiệu

Đây là chương trình giải bài toán **Word Search** (Tìm từ trong lưới chữ) sử dụng thuật toán **DFS (Depth-First Search)** cho môn **Trí tuệ nhân tạo**.

### Bài toán Word Search

- Cho một lưới chữ cái kích thước `n×n`
- Cho danh sách các từ cần tìm
- Các từ có thể nằm theo 8 hướng: ngang (trái/phải), dọc (lên/xuống), chéo (4 hướng)
- **Mục tiêu**: Tìm tất cả các từ trong lưới

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Python 3.7 trở lên
- Windows/Linux/Mac

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## 📁 Cấu trúc thư mục

```
word_search/
├── input/                      # Các test case
│   ├── easy.txt               # Dễ: 8x8, 10 từ
│   ├── medium.txt             # Trung bình: 10x10, 16 từ
│   └── hard.txt               # Khó: 12x12, 11 từ
├── src/                        # Mã nguồn
│   ├── grid.py                # Quản lý lưới
│   ├── word_search_dfs.py     # Thuật toán DFS
│   └── word_search_bfs.py     # Thuật toán BFS (bonus)
├── main.py                    # Chương trình chính
├── demo.py                    # Demo tự động
├── benchmark.py               # Đo hiệu năng
└── README.md                  # Tài liệu
```

## 💻 Cách chạy chương trình

### 1. Chạy chương trình chính (Interactive)

```bash
python -X utf8 main.py
```

**Menu chương trình:**
- `1`: Chạy test Easy (8x8)
- `2`: Chạy test Medium (10x10)
- `3`: Chạy test Hard (12x12)
- `4`: Tạo lưới ngẫu nhiên
- `5`: Tải lưới từ file
- `6`: So sánh hiệu năng
- `0`: Thoát

### 2. Chạy demo tự động

```bash
python -X utf8 demo.py
```

Chương trình sẽ tự động chạy qua tất cả test cases và hiển thị kết quả.

### 3. Chạy benchmark (đo hiệu năng)

```bash
python -X utf8 benchmark.py
```

Kết quả sẽ được lưu vào file JSON với timestamp.

## 📝 Format file input

```
<kích thước lưới>
<hàng 1: các ký tự cách nhau bởi dấu cách>
<hàng 2: các ký tự cách nhau bởi dấu cách>
...
<hàng n>
<danh sách từ cách nhau bởi dấu phẩy>
```

### Ví dụ file input:

```
5
H E L L O
W O R L D
P Y T H O
N J A V A
X Y Z A B
HELLO,WORLD,PYTHON,JAVA
```

## 🔍 Thuật toán DFS

### Nguyên lý hoạt động

1. **Quét lưới**: Tìm ký tự đầu tiên của từ cần tìm
2. **Thử 8 hướng**: Từ vị trí đó, thử tìm kiếm theo 8 hướng
3. **DFS đệ quy**: Tiếp tục tìm ký tự tiếp theo theo hướng đã chọn
4. **Backtrack**: Nếu không tìm thấy, quay lại và thử hướng khác

### Độ phức tạp

- **Thời gian**: O(N×M×8×L)
  - N×M: kích thước lưới
  - 8: số hướng
  - L: độ dài trung bình của từ
  
- **Không gian**: O(L) 
  - L: độ dài từ dài nhất (cho stack đệ quy)

### Pseudocode

```
function DFS_SEARCH(word, row, col, direction, index, path):
    if index == length(word):
        return path  // Đã tìm thấy đủ từ
    
    new_row = row + direction.dr
    new_col = col + direction.dc
    
    if not is_valid(new_row, new_col):
        return None
    
    if grid[new_row][new_col] != word[index]:
        return None
    
    return DFS_SEARCH(word, new_row, new_col, direction, index+1, path + [(new_row, new_col)])
```

## 📊 Kết quả mẫu

```
============================================================
KẾT QUẢ
============================================================
✅ Tìm thấy: 10/10 từ
⏱️  Thời gian: 0.000838 giây
💾 Bộ nhớ: 0.0034 MB
🔢 Số node đã duyệt: 135
⚡ Tốc độ: 161089 nodes/giây
```

## 🎯 Tính năng

✅ Tìm kiếm theo 8 hướng  
✅ Hiển thị step-by-step (từng bước)  
✅ Visualize kết quả với highlight  
✅ Đo thời gian và bộ nhớ chính xác  
✅ So sánh hiệu năng nhiều test case  
✅ Tạo lưới ngẫu nhiên  
✅ Lưu/tải file input  
✅ Xuất kết quả dạng JSON  

## 📈 Dữ liệu cho báo cáo

Chạy `benchmark.py` để lấy dữ liệu:

- Bảng so sánh thời gian thực thi
- Bảng so sánh bộ nhớ sử dụng
- Bảng hiệu quả tìm kiếm
- File JSON chứa chi tiết kết quả

## ⚠️ Lưu ý

1. **Encoding**: Luôn chạy với flag `-X utf8` để hỗ trợ tiếng Việt:
   ```bash
   python -X utf8 main.py
   ```

2. **Input file**: Đảm bảo mỗi hàng có đúng số ký tự theo kích thước lưới

3. **Test case**: Bạn có thể tạo thêm test case riêng trong thư mục `input/`

## 🐛 Troubleshooting

### Lỗi encoding
```
UnicodeEncodeError: 'charmap' codec can't encode character
```
**Giải pháp**: Chạy với `-X utf8`:
```bash
python -X utf8 main.py
```

### Lỗi IndexError
```
IndexError: list index out of range
```
**Giải pháp**: Kiểm tra file input có đủ số ký tự mỗi hàng không

## 📞 Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Python version >= 3.7
2. File input có đúng format không
3. Đã cài đặt requirements.txt chưa

## 📚 Tham khảo

- Tài liệu môn học Trí tuệ nhân tạo
- Thuật toán DFS: [Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- Word Search puzzle: [Puzzle-Pipes](https://www.puzzle-pipes.com/)
