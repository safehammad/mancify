from itertools import chain, islice

from nltk.tokenize import wordpunct_tokenize

import manc


def translate(text):
    """Translate from plain English to Manc."""
    tokens = tokenize(text)
    translated = substitute(tokens)
    return list(translated)


def substitute(tokens):
    """Generator producing Manc words for given tokens.
    
    Algorithm:
        1. Try direct word substitution
        2. If (1) fails, try phonetic substitution.
        3. If (2) fails, it's a symbol! Return as is...

    """
    for token in tokens:
        substitution = manc.replace_random(token)
        if substitution != token:
            yield substitution
        else:
            # TODO: alter pronunciation
            yield token


def tokenize(text):
    """Turn a block of text and tokenize into a list of words and symbols.

    Features:
      - Retain newlines.
      - Retain special characters.

    """
    lines = (line for line in text.split('\n'))
    tokens = (wordpunct_tokenize(line) + ['\n'] for line in lines)
    return list(chain.from_iterable(tokens))[:-1]
