import pandas as pd
import re
import json

# Load verbs data
with open('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/data/vn/verbs.json', 'r') as file:
    verbs = json.load(file)

# Assuming categories.json is properly structured and loaded
with open('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/data/vn/categories.json', 'r') as file:
    categories = json.load(file)

def table_data(tagged_line):
    df = pd.DataFrame(columns=["Loại phương thức thanh toán", "Loại sản phẩm", "Giá tiền", "Ngày", "Ghi chú", "Nơi mua"])

    def determine_payment_type(verb):
        for action in verbs['chi']:
            if action in verb:
                return 'Chi'
        for action in verbs['thu']:
            if action in verb:
                return 'Thu'
        return 'Khác'

    def categorize_item(item, payment_type):
        for category, items in categories.get(payment_type, {}).items():
            if item.lower() in [i.lower() for i in items]:
                return category
        return 'khác'

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
        
        return detected_money

    items = [match.split('/')[0] for match in re.findall(r'\b\w+/Item\b', tagged_line)]
    print(items)
    places = [match.split('/')[0] for match in re.findall(r'\b\w+/Place\b', tagged_line)]
    verb = [match.split('/')[0] for match in re.findall(r'\b\w+/V\b', tagged_line)]
    print( verb)
    payment_type = determine_payment_type(verb)

    money_matches = re.findall(r'\b(\d+(?:[.,]\d+)?)\b/Nu (tr|k|triệu|đ)/Money|\b(\d+(?:[.,]\d+)?)\b/Money', tagged_line)
    money_list = extract_money(money_matches)

    for idx, item in enumerate(items):
        categorized_product = categorize_item(item, payment_type)
        money = money_list[idx] if idx < len(money_list) else None
        place_of_purchase = places[0] if places else "Unknown"  # Assuming all items are bought at the same place if multiple places are not specified

        df = df.append({
            "Loại sản phẩm": categorized_product,
            "Loại phương thức thanh toán": payment_type,
            "Giá tiền": money,
            # "Ngày": pd.Timestamp.now(),   
            "Ghi chú": f"Item: {item}, Payment Method: {payment_type}",
            "Nơi mua": place_of_purchase
        }, ignore_index=True)

    return df

# Example usage:
tagged_line = "đi/V chợ/Place bán/V 100/Nu k/Money cà_phê/Item ./. mua/V dầu_gội_đầu/Item 10/Money ./."
df = table_data(tagged_line)
print(df)
