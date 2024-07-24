from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from SCRDRlearner import SCRDRTree, Node, Object  # Thay thế 'your_module_name' bằng tên module của bạn

def evaluate_model(y_true, y_pred):
    # Độ chính xác
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    # Precision, Recall, và F1-Score
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")

    # Ma trận nhầm lẫn
    conf_matrix = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(conf_matrix)

def count_nodes_and_depth(tree_root):
    def traverse(node, current_depth=0):
        nonlocal max_depth, total_nodes
        total_nodes += 1
        max_depth = max(max_depth, current_depth)
        if node.exceptChild:
            traverse(node.exceptChild, current_depth + 1)
        if node.elseChild:
            traverse(node.elseChild, current_depth)

    max_depth = 0
    total_nodes = 0
    traverse(tree_root)
    return total_nodes, max_depth

# Tạo mô hình và tải dữ liệu ở đây
tree = SCRDRTree()  # Bạn cần khởi tạo cây SCRDR của bạn
tree.constructSCRDRtreeFromRDRfile('your_rules_file.rdr')  # Nạp dữ liệu quy tắc nếu có

# Giả sử y_true và y_pred được lấy từ kết quả phân tích cú pháp thực tế và dự đoán
y_true = []  # Nhãn thực tế
y_pred = []  # Nhãn dự đoán

# Đánh giá mô hình
evaluate_model(y_true, y_pred)

# Đếm số nút và độ sâu
total_nodes, max_depth = count_nodes_and_depth(tree.root)
print(f"Total nodes in SCRDR Tree: {total_nodes}")
print(f"Maximum depth of SCRDR Tree: {max_depth}")
