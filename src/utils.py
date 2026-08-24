import re
import spacy

#load spacy nlp
nlp = spacy.load("en_core_web_sm")

#locate end of header and start of footer 
header_pattern = r"^\*{3} START OF THE PROJECT GUTENBERG EBOOK .+ \*{3}$"
footer_pattern = r"^\*{3} END OF THE PROJECT GUTENBERG EBOOK .+ \*{3}$"


def clean_book(text: str, lowercase: bool = True) -> str:
    text = text.replace('\r\n', '\n')
    # Find header and footer index using regex patterns 
    header_index = re.search(header_pattern, text, re.MULTILINE).span()[1]
    footer_index = re.search(footer_pattern, text, re.MULTILINE).span()[0]
    # Remove header and footer
    text = text[header_index + 1: footer_index - 1]
    # Remove leading and trailing whitespaces
    text = text.strip()
    # Merge consecutive whitespaces into a single one
    text = re.sub(r" +", " ", text)
    # Transform the text to lowercase precize false when not needed 
    if lowercase:
        text = text.lower()
    
    return text

def parse(text: str) -> spacy.tokens.Doc:
    return nlp(text)

def tokenize(text: str) -> spacy.tokens:
    #tokenize
    doc = nlp(text)
    tokens = [token for token in doc if not token.is_stop and not token.is_punct and not token.is_space and token.is_alpha]
    return tokens 


