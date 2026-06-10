from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer

from src.utils import  clean_book
from src.client import get_book_text

def summarize (book_id : str, target_sentences = 9) -> str:
    text = get_book_text(book_id)
    text = clean_book(text)
    #sumy expects raw text parser
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    #initialize LSA summarizer
    summarizer = LsaSummarizer(Stemmer("english"))
    #generate summary
    summary = summarizer(parser.document, target_sentences)
    return " ".join(str(sentence) for sentence in summary ) 