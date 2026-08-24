from src.utils import tokenize, clean_book
from src.client import get_book_text


def lexdiv(book_id: str) -> dict:
    text = get_book_text(book_id)    
    text = clean_book(text)
    tokens = tokenize(text)
    number_of_word_tokens = len(tokens)
    number_of_unique_word_tokens = len(set(tokens))
    measurements = {
            "tok": number_of_word_tokens,
            "typ": number_of_unique_word_tokens,
            "ttr": number_of_unique_word_tokens / number_of_word_tokens,
            "mwl": sum(len(t) for t in tokens) / number_of_word_tokens,
            "mwf": number_of_word_tokens / number_of_unique_word_tokens
            }        
    return measurements



