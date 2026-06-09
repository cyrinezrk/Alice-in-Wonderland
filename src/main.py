import argparse
from src.services.lexdiv import lexdiv
from src.services.topics import topics
from src.services.entities import entities

# Initialize parser
parse = argparse.ArgumentParser()

# Add argumnets
parse.add_argument("--lexdiv", help=f"Get metrics about the book's vocabulary")
parse.add_argument("--topics", help=f"Get the main themes that emerge across a book")
parse.add_argument("--entities", help=f"Get the characters and locations in a book")
arguments = parse.parse_args()

if arguments.lexdiv:
    print(lexdiv(arguments.lexdiv))

if arguments.topics:
    print(topics(arguments.topics))

if arguments.entities:
    print(entities(arguments.entities))
