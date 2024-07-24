from underthesea import word_tokenize, sent_tokenize
from pyvi import ViTokenizer, ViPosTagger
from pyvi import ViUtils





# Đường dẫn tới file chứa danh sách các từ cố định

fixed_words_path = 'data/vn/fixed_words.txt'
fixed_words = []

# Đọc các từ cố định từ file
with open(fixed_words_path, 'r', encoding='utf-8') as f:
    fixed_words = [line.strip() for line in f.readlines()]

# Đọc nội dung từ file input
file_path = 'data/vn/input.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Phân tách đoạn văn thành các câu

# sentences=ViTokenizer.tokenize(text)

sentences = sent_tokenize(text)
print("Các câu:", sentences)

output_path = 'data/vn/output.txt'  # Đường dẫn tới file output

# Mở file để ghi kết quả
with open(output_path, 'w', encoding='utf-8') as output_file:
    # output_file.write("Các câu:\n")
    # output_file.write("\n".join(sentences) + "\n\n")
    
    # Phân tích từ cho mỗi câu và ghi vào file
    for sentence in sentences:
        words = word_tokenize(sentence, format="text", fixed_words=fixed_words)
        output_file.write(words + "\n")

print("Đã lưu kết quả vào:", output_path)
