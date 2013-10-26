from itertools import chain

from nltk.tokenize import wordpunct_tokenize


def translate(text):
    """Translate from plain English to Manc."""
    tokens = tokenize(text)
    # TODO translate tokens into Manc :)
    return tokens


def tokenize(text):
    """Turn a block of text and tokenize into a list of words and symbols.

    Features:
      - Retain newlines.
      - Retain special characters.

    """
    lines = (line for line in text.split('\n'))
    tokens = (wordpunct_tokenize(line) + ['\n'] for line in lines)
    return list(chain.from_iterable(tokens))[:-1]
