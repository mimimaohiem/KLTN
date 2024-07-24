from fastapi import HTTPException

def get_fixed_words():
    fixed_words_path = '../data/vn/fixed_words_2.txt'
    fixed_words = []
    try:
        with open(fixed_words_path, 'r', encoding='utf-8') as f:
            fixed_words = [line.strip() for line in f.readlines()]
        return fixed_words
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Fixed words file not found")
