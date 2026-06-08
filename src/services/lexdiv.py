from src.utils import tokenize, clean_book
from src.client import get_book_text


def _calculate_hap(tokens) -> int:
    count = 0
    for token in tokens:
        if tokens.count(token) == 1:
            count += 1
    return count


def lexdiv(book_id: str) -> dict:
    text = get_book_text(book_id)    
    text = clean_book(text)
    tokens = tokenize(text)
    number_of_word_tokens = len(tokens)
    number_of_unique_word_tokens = len(set(tokens))
    measurements = {
            "tok": number_of_words_tokens,
            "typ": number_of_unique_words_tokens,
            "hap": _calculate_hap(tokens),
            }        
    return measurements



