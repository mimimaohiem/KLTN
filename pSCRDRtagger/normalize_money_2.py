import re

# Dữ liệu mẫu với các ví dụ số thập phân sử dụng dấu chấm và dấu phẩy
data = """
mua/V 10/Nu l/M dầu/Item hết/Prep 100,5/Nu k/Money kkk/Prep ./.
mua/V 10/Nu l/M dầu/Item hết/Prep 100.75/Money kkk/Prep ./.
mua/V 10/Nu kg/M muối/Item kkk/Prep ./.
Mua/V gạo/Item 10/Nu kg/M 400,25/Money ./.
Mua/V gạo/Item 10/Nu kg/M 400.50/Nu tr/Money ./.
Mua/V gạo/Item 10/Nu kg/M 500/Money ./.
Cà_phê/Item sáng/Time 15,000.99/Money ./.
Mua/V bánh_mì/Item 25,000.75/Nu đ/Money ./.
Mua/V bánh_mì/Item 500000/Money ./.
Mua/V 50/Nu tr/Money cafe/Item ./.
50/Nu k/Money cafe/Item ./.
hôm_nay/Time 500000/Money cafe/Item ./.
sáng/Time 500000/Money cafe/Item ./.
Mua/V 2,5000/Nu tr/Money bánh_mì/Item ./.
"""

# Biểu thức chính quy để tìm số tiền với và không với đơn vị đo lường
money_pattern_with_unit = re.compile(
    r'\b(\d+(?:[.,]\d+)?)\b/Nu (tr|k|triệu|đ)/Money|\b(\d+(?:[.,]\d+)?)\b/Money'
)

# Hàm để lọc số tiền từ dữ liệu
def extract_money(data):
    detected_money = []
    matches_with_unit = money_pattern_with_unit.findall(data)
    for match in matches_with_unit:
        if match[1]:  # Nếu có đơn vị tiền tệ
            amount = float(match[0].replace(',', '.'))  # Chuyển dấu phẩy thành dấu chấm nếu có
            unit = match[1]
            if unit.lower() == 'k':
                amount *= 1000
            elif unit.lower() == 'tr' or unit.lower() == 'triệu':
                amount *= 1000000
            detected_money.append(int(amount))  # Chuyển về kiểu int
        else:  # Không có đơn vị tiền tệ
            amount = float(match[2].replace(',', '.'))
            if amount < 1000:  # Nếu số tiền nhỏ hơn 1000
                amount *= 1000
            detected_money.append(int(amount))  # Chuyển về kiểu int

    return detected_money

# Lấy số tiền từ dữ liệu
detected_money = extract_money(data)
print(detected_money)
