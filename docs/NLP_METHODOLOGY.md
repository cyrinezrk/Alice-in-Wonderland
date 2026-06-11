# NLP Methodology Documentation
## Alice's Adventures in Wonderland - Book Card Engine

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Summarization Pipeline](#2-summarization-pipeline)
3. [Topic Modeling Pipeline](#3-topic-modeling-pipeline)
4. [Named Entity Recognition Pipeline](#4-named-entity-recognition-pipeline)
5. [Library Comparison & Justification](#5-library-comparison--justification)
6. [Method Trade-offs Analysis](#6-method-trade-offs-analysis)
7. [Architectural Decisions](#7-architectural-decisions)

---

## 1. Project Overview

This NLP engine transforms raw book text from Project Gutenberg into structured "book cards" containing:
- Lexical diversity metrics
- Topic modeling results
- Named entities (characters, locations)
- Intelligent summaries
- Similar book recommendations

### Core Constraints
- **No heavy models** (LLMs, large transformers, APIs forbidden)
- **Lightweight execution** (must run on any machine)
- **Explainable methods** (must justify every choice)

---

## 2. Summarization Pipeline

### 2.1 Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SUMMARIZATION PIPELINE                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   FETCH      │     │   CLEAN      │     │   PARSE      │     │  SUMMARIZE   │
│   Book Text  │────▶│   Text       │────▶│   Sentences  │────▶│  (LexRank)   │
│   (Gutenberg)│     │   (Remove    │     │   (Tokenizer)│     │              │
└──────────────┘     │   headers)   │     └──────────────┘     └──────┬───────┘
                     └──────────────┘                                  │
                                                                       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   OUTPUT     │     │   GENERATE   │     │   EXTRACT    │     │   RANK       │
│   Structured │◀────│   Summary    │◀────│   Themes     │◀────│   Sentences  │
│   Summary    │     │   Text       │     │   (Freq.)    │     │   (Top 9)    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                            ▲
                            │
              ┌─────────────┴─────────────┐
              │     ENTITY ENRICHMENT     │
              │  - Protagonist detection  │
              │  - Location extraction    │
              │  - Key sentence (Luhn)    │
              └───────────────────────────┘
```

### 2.2 Step-by-Step Process

#### Step 1: Text Acquisition
```python
text = get_book_text(book_id)  # Fetch from Project Gutenberg API
```
- Uses `httpx` client for HTTP requests
- Handles 404 errors gracefully

#### Step 2: Text Cleaning
```python
text = clean_book(text)
```
- Removes Gutenberg headers/footers using regex patterns
- Normalizes whitespace
- Optionally lowercases text

#### Step 3: Sentence Parsing (Sumy)
```python
parser = PlaintextParser.from_string(text, Tokenizer("english"))
```
- Tokenizes text into sentences
- Prepares document structure for summarization algorithms

#### Step 4: LexRank Summarization
```python
summarizer = LexRankSummarizer(Stemmer("english"))
sentences = summarizer(parser.document, target_sentences=9)
```
- Builds sentence similarity graph
- Applies eigenvector centrality (like PageRank)
- Selects top-ranked sentences

#### Step 5: Entity Integration
```python
ents = entities(book_id)
characters = clean_entities(ents["characters"])
locations = clean_entities(ents["locations"])
```
- Extracts protagonist (first/most frequent character)
- Identifies primary location
- Filters noise entities

#### Step 6: Theme Extraction
```python
freq = {}  # Word frequency analysis
for w in all_words:
    if len(w) > 2 and w not in stop:
        freq[w] = freq.get(w, 0) + 1
themes = sorted(freq, key=lambda w: -freq[w])[:2]
```
- Analyzes word frequency in extracted sentences
- Removes stopwords and noise
- Selects top 2 thematic words

#### Step 7: Summary Generation
```python
return (
    f"This literary piece follows {heros} in the unique world of {lieu}. "
    f"Exploring core themes like '{theme1}' and '{theme2}', the story is..."
)
```
- Constructs human-readable summary
- Integrates entities, themes, and key excerpt

### 2.3 Method Comparison: Why LexRank?

| Method | Algorithm | Strengths | Weaknesses | Our Choice |
|--------|-----------|-----------|------------|------------|
| **LexRank** | Graph-based (eigenvector centrality) | Handles redundancy well, captures central ideas | Slower on very long texts | **SELECTED** |
| **TextRank** | Graph-based (PageRank) | Simple, effective | Less robust to noise | Considered |
| **LSA** | Matrix factorization (SVD) | Captures latent semantics | May lose coherence | Tested |
| **Luhn** | Statistical (word frequency) | Very fast, simple | Misses context | Used for key sentence |
| **KL-Sum** | Information theory | Good diversity | Complex tuning | Not used |

#### Why LexRank over TextRank?

```
                    TEXTRANK                          LEXRANK
                    ────────                          ───────
Similarity:         Cosine (word overlap)            Cosine + IDF weighting
Graph:              Sparse connections               Dense with threshold
Ranking:            PageRank                         Eigenvector centrality
Redundancy:         May select similar sentences     Better diversity
```

**Decision**: LexRank handles literary texts better because:
1. IDF weighting reduces impact of common words ("said", "was")
2. Threshold-based graph construction improves sentence diversity
3. More robust to the varied sentence lengths in novels

### 2.4 Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **BERT/Transformers** | Too heavy (500MB+ models), violates project constraints |
| **GPT/LLM APIs** | Explicitly forbidden, not self-contained |
| **Abstractive (T5, BART)** | Heavy models, may hallucinate content |
| **Simple TF-IDF** | No sentence coherence, just keyword extraction |
| **Lead-based** | Just takes first sentences, misses structure |

---

## 3. Topic Modeling Pipeline

### 3.1 Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TOPIC MODELING PIPELINE                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   FETCH      │     │   CLEAN &    │     │   TOKENIZE   │     │   BUILD      │
│   Book Text  │────▶│   LOWERCASE  │────▶│   (spaCy)    │────▶│   DICTIONARY │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                │                      │
                     Remove:                    │                      │
                     - Headers/footers          ▼                      ▼
                     - Extra whitespace   ┌──────────────┐     ┌──────────────┐
                                          │   FILTER     │     │   CREATE     │
                                          │   TOKENS     │     │   CORPUS     │
                                          │  - Stopwords │     │   (BoW)      │
                                          │  - Punct     │     └──────────────┘
                                          │  - Non-alpha │             │
                                          └──────────────┘             │
                                                                       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   OUTPUT     │     │   FORMAT     │     │   EXTRACT    │     │   TRAIN      │
│   {1: [...]} │◀────│   TOPICS     │◀────│   TOP 10     │◀────│   LDA        │
│              │     │   Dict       │     │   WORDS      │     │   MODEL      │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### 3.2 Step-by-Step Process

#### Step 1: Tokenization with spaCy
```python
tokens = [token for token in doc
          if not token.is_stop
          and not token.is_punct
          and not token.is_space
          and token.is_alpha]
```

**Why spaCy for tokenization?**
- Linguistic awareness (POS, lemmas available)
- Built-in stopword detection
- Handles contractions properly ("don't" -> "do", "n't")

#### Step 2: Dictionary Creation (Gensim)
```python
dictionary = corpora.Dictionary([tokens_text])
```
- Maps words to unique integer IDs
- Enables efficient BoW representation

#### Step 3: Corpus Building
```python
corpus = [dictionary.doc2bow(tokens_text)]
```
- Bag-of-Words representation
- Format: [(word_id, count), ...]

#### Step 4: LDA Training
```python
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
```
- Latent Dirichlet Allocation
- Discovers latent topic distributions

#### Step 5: Topic Extraction
```python
for topic_id, topic_words in lda.print_topics():
    words = [word.split("*")[1].strip('"') for word in topic_words.split("+")]
    topics[topic_id + 1] = words
```

### 3.3 Method Comparison: LDA vs LSA

| Aspect | LDA | LSA |
|--------|-----|-----|
| **Mathematical basis** | Probabilistic (Dirichlet) | Linear algebra (SVD) |
| **Interpretability** | Topics as word distributions | Abstract dimensions |
| **Assumptions** | Documents mix topics | Linear term relationships |
| **Handles polysemy** | Better | Worse |
| **Speed** | Slower (iterative) | Faster (matrix ops) |
| **Coherent topics** | More interpretable | May be abstract |

**Decision**: We chose **LDA** because:
1. Topics are interpretable word distributions
2. Better for narrative texts with mixed themes
3. Gensim implementation is efficient and well-documented
4. Project requires human-readable topic words

### 3.4 Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **BERTopic** | Requires heavy transformer embeddings |
| **NMF** | Good alternative, but LDA more established for text |
| **HDP** | Non-parametric, harder to control topic count |
| **Word2Vec clustering** | Doesn't give topic-word distributions directly |

---

## 4. Named Entity Recognition Pipeline

### 4.1 Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ENTITY RECOGNITION PIPELINE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   FETCH      │     │   CLEAN      │     │   PARSE      │     │   EXTRACT    │
│   Book Text  │────▶│   (Keep Case)│────▶│   (spaCy)    │────▶│   ENTITIES   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                            │                    │                     │
                            ▼                    ▼                     ▼
                     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
                     │  PRESERVE    │     │   NER MODEL  │     │   FILTER BY  │
                     │  UPPERCASE   │     │  en_core_web │     │   LABEL      │
                     │  (Names!)    │     │     _sm      │     │              │
                     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                          ┌────────────────────────────┴───┐
                                          │                                │
                                          ▼                                ▼
                                   ┌──────────────┐                ┌──────────────┐
                                   │   PERSON     │                │  LOC/FAC/GPE │
                                   │   Labels     │                │   Labels     │
                                   │  (Characters)│                │  (Locations) │
                                   └──────────────┘                └──────────────┘
                                          │                                │
                                          ▼                                ▼
                                   ┌──────────────┐                ┌──────────────┐
                                   │  DEDUPLICATE │                │  DEDUPLICATE │
                                   │  (dict.from  │                │  (dict.from  │
                                   │   keys)      │                │   keys)      │
                                   └──────────────┘                └──────────────┘
                                          │                                │
                                          └────────────────┬───────────────┘
                                                           ▼
                                                    ┌──────────────┐
                                                    │   OUTPUT     │
                                                    │ {"characters"│
                                                    │  "locations"}│
                                                    └──────────────┘
```

### 4.2 Step-by-Step Process

#### Step 1: Text Cleaning (Case-Sensitive)
```python
text = clean_book(text, lowercase=False)  # CRITICAL: Keep original case
```
**Why preserve case?** NER relies on capitalization to identify proper nouns.

#### Step 2: spaCy Processing
```python
doc = parse(text)  # nlp(text) internally
```
- Applies full NLP pipeline: tokenization, POS, NER
- Uses `en_core_web_sm` model (small but effective)

#### Step 3: Entity Filtering
```python
for ent in doc.ents:
    if ent.label_ == "PERSON":
        characters.append(ent.text)
    if ent.label_ in ("LOC", "FAC", "GPE"):
        locations.append(ent.text)
```

**Entity Labels Used:**
| Label | Meaning | Example |
|-------|---------|---------|
| PERSON | People, characters | "Alice", "Queen of Hearts" |
| LOC | Natural locations | "the forest", "the river" |
| FAC | Buildings, facilities | "the palace", "the courthouse" |
| GPE | Geopolitical entities | "Wonderland", "England" |

#### Step 4: Deduplication
```python
characters = list(dict.fromkeys(characters))  # Preserves order, removes duplicates
```

### 4.3 Why spaCy?

| Library | Model Size | Speed | Accuracy | Ease of Use |
|---------|------------|-------|----------|-------------|
| **spaCy (en_core_web_sm)** | 12 MB | Fast | Good | Excellent |
| spaCy (en_core_web_lg) | 560 MB | Medium | Better | Good |
| Flair | 400+ MB | Slow | Excellent | Medium |
| Stanza | 200+ MB | Medium | Excellent | Good |
| NLTK NER | Small | Fast | Poor | Complex |

**Decision**: `en_core_web_sm` chosen because:
1. **Lightweight** (12MB) - meets project constraints
2. **Fast** - suitable for processing entire books
3. **Good accuracy** - sufficient for character/location extraction
4. **Simple API** - `doc.ents` gives all entities directly

### 4.4 Limitations & Mitigations

| Limitation | Mitigation |
|------------|------------|
| May miss uncommon names | Context helps (surrounding text) |
| False positives on titles | Noise filtering in summarize.py |
| Splits multi-word names | Post-processing could merge |
| Victorian language challenges | Model handles reasonably well |

---

## 5. Library Comparison & Justification

### 5.1 Core Libraries Used

| Library | Purpose | Version | Justification |
|---------|---------|---------|---------------|
| **sumy** | Summarization | 0.12.0 | Multiple algorithms, lightweight, well-maintained |
| **spaCy** | NLP processing | 3.x | Industry standard, fast, good NER |
| **gensim** | Topic modeling | 4.x | Best LDA implementation, efficient |
| **NLTK** | Tokenization support | 3.9.x | Sumy dependency, mature |

### 5.2 Why Sumy for Summarization?

```
┌─────────────────────────────────────────────────────────────────┐
│                    LIBRARY COMPARISON                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   SUMY (Selected)          │   Alternatives                     │
│   ═══════════════          │   ════════════                     │
│   + Multiple algorithms    │                                    │
│   + Lightweight (<5MB)     │   transformers: 500MB+ models     │
│   + Pure Python            │   gensim.summarize: Deprecated     │
│   + Active maintenance     │   PyTextRank: Heavier deps         │
│   + Easy to extend         │   summa: Less maintained           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Why spaCy over NLTK for NER?

| Feature | spaCy | NLTK |
|---------|-------|------|
| NER quality | Production-grade | Basic chunking |
| Speed | Optimized (Cython) | Pure Python |
| API | Modern, intuitive | Verbose |
| Models | Pre-trained, downloadable | Requires manual setup |
| Pipeline | Integrated | Separate tools |

### 5.4 Dependency Graph

```
bookworm.py
    │
    ├── src/services/summarize.py
    │       ├── sumy (LexRank, Luhn)
    │       ├── src/utils.py (spaCy)
    │       └── entities.py
    │
    ├── src/services/topics.py
    │       ├── gensim (LDA)
    │       └── src/utils.py (spaCy)
    │
    ├── src/services/entities.py
    │       └── src/utils.py (spaCy)
    │
    └── src/services/lexdiv.py
            └── src/utils.py (spaCy)
```

---

## 6. Method Trade-offs Analysis

### 6.1 Extractive vs Abstractive Summarization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXTRACTIVE vs ABSTRACTIVE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   EXTRACTIVE (Our Choice)           ABSTRACTIVE                             │
│   ══════════════════════            ═══════════                             │
│                                                                              │
│   ✓ Preserves author's voice        ✗ May lose original style              │
│   ✓ No hallucination risk           ✗ Can generate false info              │
│   ✓ Lightweight models              ✗ Requires heavy transformers          │
│   ✓ Deterministic output            ✗ Stochastic generation                │
│   ✓ Fast execution                  ✗ Slow inference                       │
│   ✓ Explainable process             ✗ Black-box neural nets                │
│                                                                              │
│   ✗ May lack coherence              ✓ More fluent text                     │
│   ✗ Limited compression             ✓ Higher compression ratio             │
│   ✗ Sentence boundaries fixed       ✓ Flexible phrasing                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

DECISION: Extractive chosen due to:
  1. Project constraint: No heavy models
  2. Literary texts: Author's language matters
  3. Reliability: No risk of generating false content
```

### 6.2 Graph-based vs Statistical Summarization

```
                    Graph-Based                    Statistical
                    (LexRank/TextRank)             (Luhn/TF-IDF)
                    ══════════════════             ═════════════
Principle:          Sentence similarity            Word frequency
                    + centrality ranking           + significance

Computation:        O(n²) sentence pairs           O(n) linear
                    Matrix operations              Simple counts

Quality:            Better coherence               May miss context
                    Captures relationships         Independent sentences

Our Usage:          Main summarization             Key sentence extraction
                    (LexRank)                      (Luhn)
```

### 6.3 Quality vs Speed Trade-off

```
Quality ▲
        │
        │     ● BERT-based (forbidden)
        │
        │           ● LexRank (selected)
        │       ● TextRank
        │
        │   ● Luhn (fast fallback)
        │
        │ ● Lead-N (baseline)
        └──────────────────────────────▶ Speed

Our approach: LexRank for quality + Luhn for speed-critical key sentence
```

---

## 7. Architectural Decisions

### 7.1 Modular Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE OVERVIEW                                │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │  bookworm.py  │
                              │    (CLI)      │
                              └───────┬───────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌───────────┐     ┌───────────┐     ┌───────────┐
            │  lexdiv   │     │  topics   │     │summarize  │
            └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
                  │                 │                 │
                  │                 │                 ├──▶ entities
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │   utils   │
                              │  (spaCy)  │
                              └─────┬─────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │  client   │
                              │  (httpx)  │
                              └───────────┘
```

### 7.2 Design Principles Applied

| Principle | Implementation |
|-----------|----------------|
| **Single Responsibility** | Each service handles one NLP task |
| **DRY** | Shared utilities in `utils.py` |
| **Dependency Injection** | Functions receive book_id, fetch internally |
| **Graceful Degradation** | Fallbacks for missing entities |
| **Configuration over Code** | Constants at module top (LANGUAGE, SENTENCES_COUNT) |

### 7.3 Why This Architecture?

1. **Testability**: Each service can be tested independently
2. **Maintainability**: Changes isolated to single modules
3. **Extensibility**: Easy to add new summarization methods
4. **Reusability**: Entities used by both `--entities` and `--summarize`

---

## Conclusion

This NLP engine demonstrates thoughtful methodology through:

1. **Method Selection**: Chose algorithms matching constraints (lightweight, explainable)
2. **Trade-off Analysis**: Balanced quality, speed, and resource usage
3. **Library Justification**: Selected mature, well-maintained tools
4. **Hybrid Approach**: Combined methods (LexRank + Luhn + Entities) for richer output
5. **Clean Architecture**: Modular design enabling future extensions

The summarization pipeline is particularly innovative in its integration of:
- Entity extraction for protagonist/location identification
- Frequency analysis for theme detection
- Multiple summarization algorithms for different purposes

This approach produces human-readable, contextual summaries while respecting all project constraints.

---

*Documentation generated for Epitech Alice in Wonderland NLP Project*
