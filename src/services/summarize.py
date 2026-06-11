import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words

from src.utils import clean_book
from src.client import get_book_text
from .entities import entities


NOISE = {
    "chapter", "down", "i.", "x.", "said", "miss", "ma", "fig", "extras",
    "beau", "dinn", "hjckrrh", "kings", "stolen", "un_important", "latitude",
    "longitude", "brandy", "esq", "latin grammar", "lobster quadrille",
    "lewis carroll", "shakespeare", "caucus", "a long tale", "beautiful soup",
    "pennyworth", "advice", "evidence", "hearthrug",
}

SYMBOL_NOISE = {"\u201c", "\u201d", "\u2018", "\u2019", "one", "two", "three", "way", "chapter"}


def clean_entities(raw: list[str]) -> list[str]:
    seen = set()
    result = []
    for e in raw:
        e = re.sub(r'\s+', ' ', e).strip()
        key = e.lower()
        if key in NOISE:
            continue
        if any(noise in key for noise in ("chapter", "\n")):
            continue
        if len(e) <= 2:
            continue
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


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


def extract_key_sentence(text: str) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LuhnSummarizer(Stemmer("english"))
    summarizer.stop_words = get_stop_words("english")
    result = summarizer(parser.document, 1)
    return str(result[0]) if result else "..."


def summarize(book_id: str) -> str:
    text = get_book_text(book_id)
    text = clean_book(text)

    ents = entities(book_id)
    characters = clean_entities(ents["characters"])
    locations   = clean_entities(ents["locations"])

    # Protagonist
    heros = characters[0] if characters else "a mysterious character"

    # Location — skip generic/language words
    location_noise = {"French", "English"}
    lieu = "a fascinating world"
    for l in locations:
        if l not in location_noise:
            lieu = l
            break

    # Key sentence via Luhn
    phrase_principale = extract_key_sentence(text)

    # Themes from extracted sentences (most frequent meaningful words)
    sentences = get_sentences(book_id)
    all_words = " ".join(sentences).lower().split()
    stop = get_stop_words("english") | SYMBOL_NOISE
    freq: dict[str, int] = {}
    for w in all_words:
        w = re.sub(r'[^a-z]', '', w)
        if len(w) > 2 and w not in stop and w.isalpha():
            freq[w] = freq.get(w, 0) + 1
    top_words = sorted(freq, key=lambda w: -freq[w])
    themes = [w for w in top_words if w not in {heros.lower(), lieu.lower()}][:2]

    theme1 = themes[0] if len(themes) > 0 else "various intrigues"
    theme2 = themes[1] if len(themes) > 1 else "unexpected twists"

    return (
        f"This literary piece follows {heros} in the unique world of {lieu}. "
        f"Exploring core themes like '{theme1}' and '{theme2}', the story is perfectly "
        f"captured by this key excerpt: \"{phrase_principale}\""
    )