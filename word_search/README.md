# Word Search Solver - DFS Algorithm

## Giới thiệu

Đây là chương trình giải bài toán **Word Search** (tìm từ trong lưới chữ cái) sử dụng thuật toán **DFS (Depth-First Search)**.

### Bài toán Word Search

Word Search là một trò chơi puzzle phổ biến trong đó:
- Cho một lưới chữ cái kích thước `n x n`
- Cho một danh sách các từ cần tìm
- Các từ có thể nằm theo 8 hướng: ngang (trái/phải), dọc (lên/xuống), chéo (4 hướng)
- Mục tiêu: Tìm tất cả các từ trong lưới

## Cấu trúc thư mục

```
word_search/
├── input/                      # Các test case
│   ├── easy.txt               # Lưới 8x8, 10 từ
│   ├── medium.txt             # Lưới 10x10, 16 từ
│   └── hard.txt               # Lưới 12x12, 14 từ
├── src/
│   ├── grid.py                # Class quản lý lưới
│   └── word_search_dfs.py     # Thuật toán DFS
├── main.py                    # Chương trình chính
├── requirements.txt           # Thư viện cần thiết
└── README.md                  # File này
```

## Cài đặt

1. Cài đặt Python 3.7 trở lên

2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

## Cách chạy

### Chạy chương trình chính

```bash
python main.py
```

### Menu chương trình

1. **Chạy test case có sẵn (Easy/Medium/Hard)**: Chạy các test case đã được chuẩn bị sẵn
2. **Tạo lưới ngẫu nhiên**: Tạo lưới Word Search với từ tùy chỉnh
3. **Tải lưới từ file**: Tải file input tùy chỉnh
4. **So sánh hiệu năng**: Chạy tất cả test case và so sánh kết quả

## Thuật toán DFS

### Nguyên lý hoạt động

1. **Tìm ký tự đầu tiên** của từ trong lưới
2. **Thử 8 hướng** từ vị trí đó
3. **DFS đệ quy**: Tiếp tục tìm kiếm theo hướng đã chọn
4. **Backtrack** nếu không tìm thấy

### Độ phức tạp

- **Thời gian**: O(N×M×8×L) trong trường hợp xấu nhất
  - N×M: kích thước lưới
  - 8: số hướng
  - L: độ dài trung bình của từ

- **Không gian**: O(L) cho stack đệ quy
  - L: độ dài từ dài nhất

## Format file input

```
<kích thước lưới>
<hàng 1: các ký tự cách nhau bởi dấu cách>
<hàng 2: các ký tự cách nhau bởi dấu cách>
...
<danh sách từ, cách nhau bởi dấu phẩy>
```

### Ví dụ

```
8
C A T D O G B P
H O U S E L K I
A M O U S E J G
T R E E V W X Y
F I S H Z A B C
B I R D E F G H
S U N M O O N I
S T A R K L M N
CAT,DOG,HOUSE,MOUSE,TREE,FISH,BIRD,SUN,MOON,STAR
```

## Tính năng

✅ Tìm kiếm từ theo 8 hướng
✅ Hiển thị step-by-step (từng bước)
✅ Visualize kết quả với highlight
✅ Đo thời gian và bộ nhớ
✅ So sánh hiệu năng các test case
✅ Tạo lưới ngẫu nhiên
✅ Lưu/tải lưới từ file

## Kết quả mẫu

```
============================================================
KẾT QUẢ
============================================================
✅ Tìm thấy: 10/10 từ
⏱️  Thời gian: 0.002145 giây
💾 Bộ nhớ: 0.0234 MB
🔢 Số node đã duyệt: 1247
```

## Tác giả

- Sinh viên: [Tên của bạn]
- MSSV: [MSSV]
- Môn học: Trí tuệ nhân tạo
- Học kỳ: 2 (2025-2026)

## Tham khảo

- Tài liệu môn học Trí tuệ nhân tạo
- Thuật toán DFS (Depth-First Search)
