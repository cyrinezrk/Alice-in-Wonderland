import argparse
from src.client import get_book_text

# Initialize parser
parse = argparse.ArgumentParser()

# Add argumnets
parse.add_argument("--lexdiv", help=f"Get metrics about the book's vocabulary")

arguments = parse.parse_args()

book_id = arguments.lexdiv

print(get_book_text(book_id))

