import re
import nltk


header_pattern = r"^\*{3} START OF THE PROJECT GUTENBERG EBOOK .+ \*{3}$"
footer_pattern = r"^\*{3} END OF THE PROJECT GUTENBERG EBOOK .+ \*{3}$"


def clean(text: str):
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

    # Transform the text to lowercase
    text = text.lower()

    return text


def tokenize(text: str):
    return


