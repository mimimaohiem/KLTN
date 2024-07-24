from underthesea import word_tokenize, sent_tokenize, text_normalize
from fastapi import HTTPException
  

def process_text(note: str):
    # Load fixed words from file
    fixed_words_path = '/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/data/vn/fixed_words_2.txt'
    try:
        with open(fixed_words_path, 'r', encoding='utf-8') as f:
            fixed_words = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Fixed words file not found")

    # Normalize and tokenize the text
    normalized_text = text_normalize(note)
    sentences = sent_tokenize(normalized_text)
    output = []
    for sentence in sentences:
        words = word_tokenize(sentence, format="text", fixed_words=fixed_words)
        output.append(words)
    
    # Combine the words into a single string
    processed_text = ' '.join(output)

    return processed_text

# note = "đi   chợ    mua 100k cà phê, dầu gội đầu 100k"
# process_text = process_text(note)
# print("Tagged text:", process_text)  # In kết quả đã gắn thẻ từ loại của câu input
