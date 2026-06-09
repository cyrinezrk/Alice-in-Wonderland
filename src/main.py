import argparse
from src.utils import clean_book, tokenize
from src.client import get_book_text
from src.services.lexdiv import lexdiv
from src.services.topics import topics

# Initialize parser
parse = argparse.ArgumentParser()

# Add argumnets
parse.add_argument("--lexdiv", help=f"Get metrics about the book's vocabulary")
parse.add_argument("--topics", help=f"Get the main themes that emerge across a book")
arguments = parse.parse_args()

if arguments.lexdiv:
    print(lexdiv(arguments.lexdiv))

if arguments.topics:
    print(topics(arguments.topics))
