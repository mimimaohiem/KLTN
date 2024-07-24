import re

def normalize_money(line):
    # Định nghĩa các hệ số
    multipliers = {
        'k': 1e3,
        'tr': 1e6,
        'triệu': 1e6,
        'đ': 1,
        'vnd': 1,
        'vnđ': 1
    }
    # Tìm tất cả các nhãn số và tiền trong dòng
    tokens = re.findall(r'(\d+(?:\.\d+)?)([a-zA-Z]*)/Nu|([a-zA-Z]+)/Money', line)
    print(tokens)
    total = 0
    previous_number = None
    previous_unit_found = False


    # for token in tokens:
    #     if '/Money' in token:

    #         number = re.search(r'(\d+(?:\.\d+)?)(?:\s*(?:k|tr|triệu|đ|vnd|vnđ))?/Money', token).group(1)
    #         total += float(number)
    #     elif '/Nu' in token:
    #         number, unit = re.match(r'(\d+(?:\.\d+)?)(?:\s*(?:k|tr|triệu|đ|vnd|vnđ))?/Nu', token).groups()
    #         total += float(number) * multipliers.get(unit, 1)

    # return total

    for groups in tokens:
        number, unit, money_unit = groups
        if number:
            # Lưu số trước nhãn Money để sử dụng nếu cần
            previous_number = float(number)
            previous_unit_found = False
            if unit:
                # Xử lý số với đơn vị nếu có
                unit = unit.lower()
                for key in multipliers:
                    if key.startswith(unit):
                        previous_number *= multipliers[key]
                        previous_unit_found = True
                        break
        elif money_unit:
            # Xử lý nhãn Money nếu nó là đơn vị
            money_unit = money_unit.lower()
            if money_unit in multipliers:
                if previous_number is not None and not previous_unit_found:
                    total += previous_number * multipliers[money_unit]
                elif previous_unit_found:
                    total += previous_number
            else:
                # Nếu nhãn Money không phải là đơn vị, coi nó là số
                total += previous_number if previous_number is not None else 0

    return total

# Ví dụ dữ liệu để kiểm tra
data_samples = [
    "mua/V 10/Nu l/Nu dầu/Item hết/Prep 100/Money kkk/Prep ./.",
    "Mua/V gạo/Item 10/Nu kg/Nu 400/Nu tr/Money ./.",
    "Mua/V bánh_mì/Item 25000/Nu d/Money ./.",
    "Mua/V 50/Nu tr/Money cafe/Item ./.",
    "1.2/Nu tr/Money ./."
]

for sample in data_samples:
    normalized_money = normalize_money(sample)
    print(f"Original: {sample}\nNormalized Money: {normalized_money}\n")
