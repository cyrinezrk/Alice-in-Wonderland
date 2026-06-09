import argparse
from src.utils import clean_book, tokenize
from src.client import get_book_text
from src.services.lexdiv import lexdiv

# Initialize parser
parse = argparse.ArgumentParser()

# Add argumnets
parse.add_argument("--lexdiv", help=f"Get metrics about the book's vocabulary")

arguments = parse.parse_args()

book_id = arguments.lexdiv

print(lexdiv(book_id))

