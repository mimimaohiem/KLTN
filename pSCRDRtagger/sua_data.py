import re

def process_line(line):
    # Sửa giá trị tiền tệ với cả "k", "triệu" và các số không có đơn vị
    line = re.sub(r'(\d+)k/Money', r'\1/Nu k/Money', line)
    line = re.sub(r'(\d+) triệu/Money', r'\1/Nu triệu/Money', line)
    line = re.sub(r'(\d+)_k/Money', r'\1/Nu k/Money', line)
    line = re.sub(r'(\d+)_triệu/Money', r'\1/Nu triệu/Money', line)
    # Xử lý trường hợp các số không có "k" hoặc "triệu" nhưng được đánh dấu là tiền tệ
    line = re.sub(r'(\d+)/Money', r'\1/Nu/Money', line)
    return line

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = [process_line(line.strip()) for line in lines]

    with open(output_filename, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line + '\n')

# Đường dẫn file input
input_filename = r'../data/vn/data_train/train_2.txt'
# Đường dẫn file output, bạn có thể thay đổi tên file này nếu muốn
output_filename = r'../data/vn/data_train/processed_train_2.txt'

process_file(input_filename, output_filename)
