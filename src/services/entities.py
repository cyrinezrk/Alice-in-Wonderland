from src.utils import clean_book, parse
from src.client import get_book_text

def entities(book_id: str) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text, lowercase = False)
    doc = parse(text)
    
    #get all entities w position and labell 
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

    characters = []
    locations = []
    for ent in doc.ents : 
        if ent.label_ == "PERSON":
            characters.append(ent.text)
        if ent.label_ in ("LOC", "FAC", "GPE"):
            locations.append(ent.text)
    return {
        "characters": list(dict.fromkeys(characters)),
        "locations": list(dict.fromkeys(locations))
    }