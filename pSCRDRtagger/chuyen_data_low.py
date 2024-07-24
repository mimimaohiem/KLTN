# -*- coding: utf-8 -*-

import os
import sys
os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("./pSCRDRtagger")




# Đọc nội dung từ file input
file_path = '../data/vn/input.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Phân tách đoạn văn thành các câu
lines = text.splitlines()
normalized_data = []

for line in lines:
    parts = line.split('/')
    parts[0] = parts[0].lower()  # Chuyển phần tử đầu tiên thành chữ thường
    normalized_line = '/'.join(parts)
    normalized_data.append(normalized_line)

# In kết quả
for line in normalized_data:
    print(line)

output_path = '../data/vn/output.txt'  # Đường dẫn tới file output

# Mở file để ghi kết quả
with open(output_path, 'w', encoding='utf-8') as output_file:
    for line in normalized_data:
        output_file.write(line + "\n")

print("Đã lưu kết quả vào:", output_path)
