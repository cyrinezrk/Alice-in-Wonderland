import argparse
from src.utils import clean_book, tokenize
from src.client import get_book_text

# Initialize parser
parse = argparse.ArgumentParser()

# Add argumnets
parse.add_argument("--lexdiv", help=f"Get metrics about the book's vocabulary")

arguments = parse.parse_args()

book_id = arguments.lexdiv

print(tokenize(clean_book(get_book_text(book_id))))

