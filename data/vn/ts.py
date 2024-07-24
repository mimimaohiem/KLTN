import os
from collections import Counter
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import MultiLabelBinarizer

# Đường dẫn tới tệp chứa nhãn thực tế và nhãn dự đoán
true_labels_path = r"./nhan_dung.txt"
predicted_labels_path = r"./output.txt.TAGGED"

# Hàm để đọc dữ liệu từ tệp
def load_labels(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    labels = [line.strip().split() for line in data if line.strip()]
    return labels

# Tải nhãn thực tế và nhãn dự đoán
y_true = load_labels(true_labels_path)
y_pred = load_labels(predicted_labels_path)

# Kiểm tra nếu số dòng trong nhãn thực tế và nhãn dự đoán không khớp
if len(y_true) != len(y_pred):
    raise ValueError("Số dòng trong nhãn thực tế và nhãn dự đoán không khớp.")

# Chuyển đổi nhãn sang định dạng nhị phân
mlb = MultiLabelBinarizer()
y_true_binary = mlb.fit_transform(y_true)
y_pred_binary = mlb.transform(y_pred)

# Phân tích nhãn dự đoán và nhãn thực tế để tính độ chính xác dựa trên cặp từ/nhãn
total_label_pairs = sum(len(line) for line in y_true)
correct_label_pairs = sum(1 for true, pred in zip(y_true, y_pred) for t, p in zip(true, pred) if t == p)

# Tính độ chính xác dựa trên cặp từ/nhãn
accuracy = correct_label_pairs / total_label_pairs

# Đếm tần suất xuất hiện của mỗi nhãn trong tập dữ liệu dự đoán
labels_count = Counter()
for line in y_pred:
    labels = [pair.split('/')[-1] for pair in line]  # Tách nhãn từ mỗi cặp
    labels_count.update(labels)

# Tổng số dòng
total_lines = len(y_pred)

# In ra các kết quả
print("Tổng số từ đã kiểm tra:", total_label_pairs)
print("Độ chính xác:", accuracy)
print("Số nhãn đúng:", correct_label_pairs)
print("Số nhãn sai:", total_label_pairs - correct_label_pairs)
print("Tổng số dòng đã kiểm tra:", total_lines)
print("Số lượng của mỗi nhãn:")
for label, count in labels_count.items():
    print(f"{label}: {count}")

# Tính toán Precision, Recall và F1-Score
all_labels = mlb.classes_
report = classification_report(y_true_binary, y_pred_binary, target_names=all_labels, zero_division=0)
print("Classification Report:\n", report)

# Hiển thị ma trận nhầm lẫn
conf_matrix = confusion_matrix(y_true_binary.argmax(axis=1), y_pred_binary.argmax(axis=1), labels=range(len(all_labels)))
print("Confusion Matrix:\n", conf_matrix)
import matplotlib.pyplot as plt

# Đếm tần suất xuất hiện của mỗi nhãn trong tập dữ liệu dự đoán
labels_count = Counter()
for line in y_pred:
    labels = [pair.split('/')[-1] for pair in line]  # Tách nhãn từ mỗi cặp
    labels_count.update(labels)

# Chuẩn bị dữ liệu cho biểu đồ
labels, frequencies = zip(*labels_count.items())

# Vẽ biểu đồ tần suất của các nhãn
plt.figure(figsize=(10, 8))
plt.bar(labels, frequencies, color='blue')
plt.xlabel('Nhãn')
plt.ylabel('Tần suất')
plt.title('Biểu đồ tần suất xuất hiện của các nhãn')
plt.xticks(rotation=45)
plt.tight_layout()  # Đảm bảo nhãn trục không bị cắt
plt.show()
