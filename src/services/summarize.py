import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer

from src.utils import clean_book
from src.client import get_book_text


def get_sentences(book_id: str, target_sentences=9) -> list[str]:
    text = get_book_text(book_id)
    text = clean_book(text)

    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # LSA method 
    # summarizer = LsaSummarizer(Stemmer("english"))

    # Luhn method 
    # summarizer = LuhnSummarizer(Stemmer("english"))

    # LexRank method
    summarizer = LexRankSummarizer(Stemmer("english"))

    sentences = summarizer(parser.document, target_sentences)

    doc_sentences = list(parser.document.sentences)
    ordered = sorted(sentences, key=lambda s: doc_sentences.index(s))

    return [str(s) for s in ordered] #convert sentence in python str


def sentences_to_paragraph(sentences: list[str]) -> str:
    #stitch sentences w these words 
    transitions = ["As the story progresses, ", "Later, ", "Meanwhile, ", "Eventually, "]
    processed = []

    for i, s in enumerate(sentences):
        #clean
        s = s.strip()
        s = re.sub(r'_([^_]+)_', r'\1', s)
        s = s[0].upper() + s[1:] if s else s

        if i == 0: #when to add the insertions words 
            processed.append(s)
        elif i == len(sentences) - 1: #lastsentence 
            processed.append("Finally, " + s[0].lower() + s[1:])
        elif i % 3 == 0:
            t = transitions[(i // 3 - 1) % len(transitions)]
            processed.append(t + s[0].lower() + s[1:]) #every 3rd sentence 
        else:
            processed.append(s)

    return " ".join(processed)


def summarize(book_id: str) -> str:

    sentences = get_sentences(book_id)
    paragraph = sentences_to_paragraph(sentences)
    return paragraph