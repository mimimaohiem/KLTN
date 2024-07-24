from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

# Giả sử y_true là nhãn thật và y_pred là nhãn dự đoán của mô hình
y_true = [...]  # Nhãn thật từ tập kiểm tra
y_pred = [...]  # Nhãn dự đoán từ mô hình

# Tính toán các chỉ số đánh giá
accuracy = accuracy_score(y_true, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
conf_matrix = confusion_matrix(y_true, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1}")
print(f"Confusion Matrix:\n{conf_matrix}")
