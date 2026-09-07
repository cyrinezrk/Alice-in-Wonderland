# Alice in Wonderland — Bookworm

NLP CLI prototype that turns public domain books (Project Gutenberg) into short "book cards": lexical diversity, topics, named entities, summary.

## 🇬🇧 About this repo

This repo was recovered from a school project (Epitech). Original repo history: ~25 commits (feature by feature). This repo only has 2 commits (`Initial commit` + `get project from school git`), so the full dev history isn't here — only the final state of the code. Some files still have Windows `:Zone.Identifier` artifacts from being copied manually instead of cloned/forked.

## 🇫🇷 À propos de ce dépôt

Ce dépôt provient d'un projet scolaire (Epitech). Le dépôt d'origine a ~25 commits (feature par feature). Ce dépôt-ci n'a que 2 commits (`Initial commit` + `get project from school git`) : l'historique de dev n'a pas été conservé, seul l'état final du code est présent. Certains fichiers gardent des artefacts Windows `:Zone.Identifier` (copie manuelle, pas un clone/fork).

## Commands

```bash
python -m src.bookworm --download <ID>    # download book from Project Gutenberg
python -m src.bookworm --lexdiv <ID>      # lexical diversity metrics
python -m src.bookworm --topics <ID>      # topic modeling (LDA)
python -m src.bookworm --entities <ID>    # named entities (characters/locations)
python -m src.bookworm --summarize <ID>   # summary (LexRank)
```

## Install

```bash
git clone https://github.com/cyrinezark/alice-in-wonderland.git
cd alice-in-wonderland
uv sync
uv run python -m spacy download en_core_web_sm
```

Python ≥ 3.13, dependency manager: `uv`. Main libs: `httpx`, `spacy`, `gensim`, `sumy`, `pydantic`.

## Structure

```
src/
├── bookworm.py       # CLI
├── client.py         # Gutenberg HTTP client
├── utils.py          # cleaning / tokenization
└── services/
    ├── lexdiv.py
    ├── topics.py
    ├── entities.py
    ├── summarize.py
    └── similar.py     # empty / not implemented
```

## Status

Prototype, school context. `similar.py` and `docs/documentation.md` are empty/unfinished.
