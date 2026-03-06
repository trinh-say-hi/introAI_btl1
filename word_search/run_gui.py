"""
Gọi GUI để trực quan hoá bài toán
Lấy danh sách đề bài từ thư mục input
Chạy GUI với danh sách vừa lấy
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from UI.gui import run_gui

def main():
    input_dir = os.path.join(os.path.dirname(__file__), "input")
    run_gui(input_dir=input_dir)


if __name__ == "__main__":
    main()
