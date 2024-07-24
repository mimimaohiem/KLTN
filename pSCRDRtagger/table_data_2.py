import pandas as pd
import re
import json

# Đọc danh sách phương thức thanh toán từ file JSON
with open('../data/vn/verbs.json', 'r') as file:
    verbs = json.load(file)

# Đọc dữ liệu từ file
with open('../data/vn/output.txt.TAGGED', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Khởi tạo DataFrame
df = pd.DataFrame(columns=["Món đồ", "Phương thức thanh toán", "Loại phương thức thanh toán", "Nơi mua", "Người thụ hưởng", "Số tiền"])

# Hàm xác định loại phương thức thanh toán
def determine_payment_type(verb):
    for action in verbs['chi']:
        if action in verb:
            return 'Chi'
    for action in verbs['thu']:
        if action in verb:
            return 'Thu'
    return 'Khác'




# Hàm để lọc số tiền từ dữ liệu
def extract_money(money_matches):
    detected_money = []
    for match in money_matches:
        amount = float(match[0].replace(',', '.')) if match[0] else float(match[2].replace(',', '.'))
        unit = match[1] if match[1] else None
        if unit:
            if unit.lower() in ['k', 'ngàn']:
                amount *= 1000
            elif unit.lower() in ['tr', 'triệu']:
                amount *= 1000000
        else:
            if amount < 1000:
                amount *= 1000
        detected_money.append(int(amount))
    return sum(detected_money)

# Xử lý từng dòng
for line in lines:
    items = [match.split('/')[0] for match in re.findall(r'\b\w+/Item\b', line)]
    verb = ' '.join([match.split('/')[0] for match in re.findall(r'\b\w+/V\b', line)])
    method = ' '.join([match.split('/')[0] for match in re.findall(r'\b\w+/Method\b', line)])
    place = ' '.join([match.split('/')[0] for match in re.findall(r'\b\w+/Place\b', line)])
    money_matches = re.findall(r'\b(\d+(?:[.,]\d+)?)\b/Nu (tr|k|triệu|đ)/Money|\b(\d+(?:[.,]\d+)?)\b/Money', line)
        
    beneficiary = ' '.join([match.split('/')[0] for match in re.findall(r'\b\w+/Person\b|\b\w+/Animal\b', line)])
    payment_type = determine_payment_type(verb)
    normalized_money = extract_money(money_matches)
    df = df.append({
        "Món đồ": ', '.join(items) if items else "N/A",
        "Phương thức thanh toán": method if method else "Tiền mặt",
        "Loại phương thức thanh toán": payment_type,
        "Nơi mua": place if place else "N/A",
        "Người thụ hưởng": beneficiary if beneficiary else "Không rõ",
        "Số tiền": normalized_money
    }, ignore_index=True)

# Lưu DataFrame vào file CSV
df.to_csv('../data/vn/processed_output.csv', index=False, encoding='utf-8')

print(f"Data has been successfully saved to ../data/vn/processed_output.csv")
print(df.head())
