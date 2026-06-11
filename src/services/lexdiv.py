from src.utils import tokenize, clean_book
from src.client import get_book_text


def lexdiv(book_id: str) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text)
    tokens = tokenize(text)

    # Convert Token objects to strings for proper comparison
    token_texts = [token.text for token in tokens]

    number_of_word_tokens = len(token_texts)
    number_of_unique_word_tokens = len(set(token_texts))

    # Calculate hapax legomena (words occurring only once)
    from collections import Counter
    word_counts = Counter(token_texts)
    hapax_count = sum(1 for count in word_counts.values() if count == 1)

    measurements = {
            "tok": number_of_word_tokens,
            "typ": number_of_unique_word_tokens,
            "hap": hapax_count,
            "ttr": number_of_unique_word_tokens / number_of_word_tokens,
            "mwl": sum(len(t) for t in token_texts) / number_of_word_tokens,
            "mwf": number_of_word_tokens / number_of_unique_word_tokens
            }
    return measurements



