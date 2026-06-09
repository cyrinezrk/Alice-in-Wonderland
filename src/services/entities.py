from src.utils import tokenize, clean_book
from src.client import get_book_text

def entities(book_id: str) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text)
    tokens = tokenize(text)
    
    for ent in tokens.ents: #token is doc object
        print(ent.text, ent.start_char, ent.end_char, ent.label_)