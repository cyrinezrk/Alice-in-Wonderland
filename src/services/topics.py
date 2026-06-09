from gensim import corpora
from gensim.models import LdaModel
from src.utils import tokenize, clean_book
from src.client import get_book_text


def topics(book_id: str) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text)
    tokens = tokenize(text)

    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(tokens)]

    lda = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=10
    )
    return lda.print_topics()