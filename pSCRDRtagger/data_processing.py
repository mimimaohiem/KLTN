import pandas as pd
import re
import json

# Load verbs data
with open('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/data/vn/verbs.json', 'r') as file:
    verbs = json.load(file)

# Load categories data (assuming it's structured correctly)
with open('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/data/vn/categories.json', 'r') as file:
    categories = json.load(file)

def table_data(tagged_lines):
    df = pd.DataFrame(columns=["Món đồ", "Phương thức thanh toán", "Loại phương thức thanh toán", "Nơi mua", "Người thụ hưởng", "Số tiền", "Loại sản phẩm"])  # Added "Loại sản phẩm"

    def determine_payment_type(verb):
        for action in verbs['chi']:
            if action in verb:
                return 'chi'
        for action in verbs['thu']:
            if action in verb:
                return 'thu'
        return 'chi'

    def extract_money(money_matches, money_matches_1):
        detected_money = []
        # Use money_matches if it's not empty, otherwise use money_matches_1
        matches = money_matches if money_matches else money_matches_1
        for match in matches:
            amount = match[0] if match[0] else match[2]
            if amount:  # Ensure the amount is not empty
                amount = float(amount.replace(',', '.'))
                unit = match[1] if match[1] else (match[3] if len(match) > 3 else None)
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

    def categorize_item(item, payment_type):
        for category, keywords in categories.get(payment_type, {}).items():
            for keyword in keywords:
                if keyword in item.lower():
                    return category
        return 'khác'

    for tagged_line in tagged_lines.split('\n'):
        tagged_line = tagged_line.strip()
        if not tagged_line:
            continue

        # Extract items and places considering separators
    
        items = []
        item_group = []
        places = []
        place_group = []
        tokens = tagged_line.split()

        for token in tokens:
            token = token.replace('_', ' ') 
            if '/Item' in token:
                item_group.append(token.replace('/Item', ''))
            elif '/Place' in token:
                place_group.append(token.replace('/Place', ''))
            elif '/Punc' in token or '/Conj' in token:
                if item_group:
                    items.append(' '.join(item_group))
                    item_group = []
                if place_group:
                    places.append(' '.join(place_group))
                    place_group = []
            else:
                if item_group:
                    items.append(' '.join(item_group))
                    item_group = []
                if place_group:
                    places.append(' '.join(place_group))
                    place_group = []

        if item_group:
            items.append(' '.join(item_group))
        if place_group:
            places.append(' '. join(place_group))

        verb = ' '.join([match.split('/')[0].lower() for match in re.findall(r'\b\w+/V\b', tagged_line)])
        method_parts = [match.split('/')[0].replace('_', ' ') for match in re.findall(r'\b\w+/Method\b', tagged_line)]
        method = ' '. join(method_parts)

        # Define regex patterns
        money_matches_1 = re.findall(r'\b(\d+(?:[.,]\d+)?)_?(tr|k|triệu|đ)?/Money', tagged_line)
        money_matches = re.findall(r'\b(\d+(?:[.,]\d+)?)\b/Nu (tr|k|triệu|đ)/Money|\b(\d+(?:[.,]\d+)?)\b/Money', tagged_line)
        beneficiary = ' '. join([match.split('/')[0] for match in re.findall(r'\b\w+/Person\b|\b\w+/Animal\b', tagged_line)])
        payment_type = determine_payment_type(verb)
        print(money_matches)
        print(money_matches_1)

        normalized_money = extract_money(money_matches, money_matches_1)
        # Categorize items
        categorized_items = [categorize_item(item, payment_type) for item in items]
        print(categorized_items)
        print(items)
    
        df = df.append({
            "Món đồ": ', '. join(items) if items else "",
            "Phương thức thanh toán": method if method else "Tiền mặt",
            "Loại phương thức thanh toán": payment_type,
            "Nơi mua": ', '. join(places) if places else "",
            "Người thụ hưởng": beneficiary if beneficiary else "Bản thân",
            "Số tiền": normalized_money,
            "Loại sản phẩm": ', '. join(categorized_items)   # Add categorized items
        }, ignore_index=True)

    return df

def save_dataframe(df, path='../data/vn/processed_output.csv'):
    df.to_csv(path, index=False, encoding='utf-8')
    print(f"Data has been successfully saved to {path}")    
    return df.head()

tagged_lines = """
thanh_toán/V tiền_điện/Item tháng/Time này/Time 5,5_tr/Money ./.
Mua/V sữa/Item cho/Prep bé/Person ở/Prep siêu_thị/Place 2.2_tr/Money ./.
cà_phê/Item với/Prep bạn/Person 50/Nu k/Money chuyển_khoản/Method ./.
mua/V trái_cây/Item ở/Prep cửa_hàng/Place 80/Nu k/Money ./.
thanh_toán/V tiền_nước/Item 300/Nu k/Money ./.
"""
df = table_data(tagged_lines)
print(df)  # In kết quả đã gắn thẻ từ loại của câu input
