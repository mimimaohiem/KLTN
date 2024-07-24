import matplotlib.pyplot as plt

# Dữ liệu hiệu suất của mô hình
metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
model_scores = [0.85, 0.83, 0.87, 0.85]

# Tạo biểu đồ cột
fig, ax = plt.subplots()
bars = ax.bar(metrics, model_scores)

# Thêm tiêu đề và nhãn
ax.set_ylabel('Scores')
ax.set_title('Performance Metrics of the Model')

# Thêm giá trị trên đỉnh các cột
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom')  # va: vertical alignment

plt.show()
