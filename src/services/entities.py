from src.utils import clean_book, parse
from src.client import get_book_text

def entities(book_id: str) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text, lowercase = False)
    doc = parse(text)
    print("entities")
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)