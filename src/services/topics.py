from gensim import corpora
from gensim.models import LdaModel
from src.utils import tokenize, clean_book
from src.client import get_book_text


def topics(book_id: str) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text)
    tokens = tokenize(text)
    tokens_text = [token.text for token in tokens] # from token obj to list of str 

    dictionary = corpora.Dictionary([tokens_text])
    corpus = [dictionary.doc2bow(tokens_text)]

    lda = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=10
    )
    return lda.print_topics()