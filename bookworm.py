#!/usr/bin/env python3
"""
BookWorm - NLP Book Card Engine
===============================
A lightweight tool that creates "book cards" from Project Gutenberg books.

Usage:
    python bookworm.py --lexdiv <ID>      # Lexical diversity metrics
    python bookworm.py --topics <ID>      # Topic modeling
    python bookworm.py --entities <ID>    # Named entity extraction
    python bookworm.py --summarize <ID>   # Book summarization
"""

import argparse
import json
from src.services.lexdiv import lexdiv
from src.services.topics import topics
from src.services.entities import entities
from src.services.summarize import summarize


def main():
    parser = argparse.ArgumentParser(
        description="BookWorm - NLP Book Card Engine for Project Gutenberg books"
    )

    parser.add_argument(
        "--lexdiv",
        metavar="ID",
        help="Get lexical diversity metrics for a book"
    )
    parser.add_argument(
        "--topics",
        metavar="ID",
        help="Extract main topics from each section of a book"
    )
    parser.add_argument(
        "--entities",
        metavar="ID",
        help="Extract characters and locations from a book"
    )
    parser.add_argument(
        "--summarize",
        metavar="ID",
        help="Generate a summary of a book"
    )

    args = parser.parse_args()

    if args.lexdiv:
        result = lexdiv(args.lexdiv)
        print(json.dumps(result, indent=2))

    elif args.topics:
        result = topics(args.topics)
        print(json.dumps(result, indent=2))

    elif args.entities:
        result = entities(args.entities)
        print(json.dumps(result, indent=2))

    elif args.summarize:
        result = summarize(args.summarize)
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
