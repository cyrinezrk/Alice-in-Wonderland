# Alice in Wonderland - NLP Book Card Engine

A lightweight NLP tool that creates "book cards" to help publishers and editors quickly understand books from Project Gutenberg without reading them entirely.

## Features

| Command | Description |
|---------|-------------|
| `--lexdiv <ID>` | Lexical diversity metrics (vocabulary richness) |
| `--topics <ID>` | Topic modeling (main themes per section) |
| `--entities <ID>` | Named entity extraction (characters, locations) |
| `--summarize <ID>` | Intelligent book summarization |

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Alice-in-Wonderland

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Usage

```bash
# Lexical diversity metrics
python bookworm.py --lexdiv 11

# Topic modeling (10 topics with top words)
python bookworm.py --topics 11

# Named entities (characters & locations)
python bookworm.py --entities 11

# Book summarization
python bookworm.py --summarize 11
```

### Example Output

**Lexical Diversity (`--lexdiv 11`):**
```json
{
  "tok": 26432,
  "typ": 2876,
  "hap": 1523,
  "ttr": 0.1088,
  "mwl": 4.32,
  "mwf": 9.19
}
```

**Summarization (`--summarize 11`):**
```
This literary piece follows Alice in the unique world of Wonderland.
Exploring core themes like 'queen' and 'time', the story is perfectly
captured by this key excerpt: "We're all mad here..."
```

## Project Structure

```
Alice-in-Wonderland/
├── bookworm.py              # CLI entry point
├── src/
│   ├── client.py            # Project Gutenberg API client
│   ├── utils.py             # Shared NLP utilities (spaCy)
│   └── services/
│       ├── lexdiv.py        # Lexical diversity metrics
│       ├── topics.py        # LDA topic modeling
│       ├── entities.py      # Named entity recognition
│       └── summarize.py     # Book summarization
├── docs/
│   └── NLP_METHODOLOGY.md   # Detailed methodology documentation
├── requirements.txt
└── README.md
```

## Supported Books

The tool works with any book from Project Gutenberg using its ID:

| ID | Title | Category |
|----|-------|----------|
| 11 | Alice's Adventures in Wonderland | Children |
| 12 | Through the Looking-Glass | Children |
| 16 | Peter Pan | Children |
| 84 | Frankenstein | Sci-Fi |
| 345 | Dracula | Sci-Fi |
| 1661 | The Adventures of Sherlock Holmes | Mystery |

## Technical Approach

### Summarization
- **Method**: LexRank (graph-based extractive)
- **Why**: Handles literary texts well, no heavy models required
- **Enhancement**: Integrates entity extraction for protagonist/location context

### Topic Modeling
- **Method**: LDA (Latent Dirichlet Allocation)
- **Library**: Gensim
- **Why**: Interpretable word distributions, efficient implementation

### Named Entity Recognition
- **Method**: spaCy NER
- **Model**: en_core_web_sm (12MB, lightweight)
- **Labels**: PERSON (characters), LOC/FAC/GPE (locations)

See [docs/NLP_METHODOLOGY.md](docs/NLP_METHODOLOGY.md) for detailed methodology, pipeline diagrams, and method comparisons.

## Dependencies

- **httpx**: HTTP client for Gutenberg API
- **spaCy**: NLP processing and NER
- **gensim**: Topic modeling (LDA)
- **sumy**: Extractive summarization algorithms
- **nltk**: Tokenization support

## License

Epitech Project - Through the Looking-Glass
