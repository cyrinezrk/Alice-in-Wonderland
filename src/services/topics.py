from gensim import corpora
from gensim.models import LdaModel
from src.utils import tokenize, clean_book
from src.client import get_book_text


def split_into_sections(tokens_text: list[str], num_sections: int = 10) -> list[list[str]]:

    if num_sections < 1:
        num_sections = 1
    section_size = max(1, len(tokens_text) // num_sections)
    sections = [
        tokens_text[i:i + section_size]
        for i in range(0, len(tokens_text), section_size)
    ]
    return sections


def topics(book_id: str, num_sections: int = 10) -> dict:
    text = get_book_text(book_id)
    text = clean_book(text)
    tokens = tokenize(text)
    tokens_text = [token.text for token in tokens]  # from token obj to list of str

    sections = split_into_sections(tokens_text, num_sections)

    dictionary = corpora.Dictionary(sections)
    corpus = [dictionary.doc2bow(section) for section in sections]

    lda = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=len(sections)
    )

    topics_by_section = {}
    for section_index, section_bow in enumerate(corpus):
        topic_distribution = lda.get_document_topics(section_bow)
        dominant_topic_id = max(topic_distribution, key=lambda pair: pair[1])[0]
        top_words = [word for word, _ in lda.show_topic(dominant_topic_id, topn=10)]
        topics_by_section[section_index + 1] = top_words

    return topics_by_section