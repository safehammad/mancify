from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')

import logging
from itertools import chain
import random
import re

import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import cmudict

from .pronunciation import pronounce, grapheme, Phoneme
from .dialects import manc


# Regex match a digit
match_digits = re.compile(r'\d')


def translate(text, dialect=manc, seed=None):
    """Translate from plain English to given dialect."""
    random.seed(seed)
    tokens = tokenize(text)
    restructured = restructure(tokens,dialect)
    translated = substitute(restructured, dialect)
    return untokenize(translated)


def restructure(tokens, dialect):
    """Rearrange the structure of the input based on the given dialect."""
    tagged = [("START","START")] + nltk.pos_tag(tokens) + [("END","END")]
    logging.debug("Tagged=%s", tagged)
    for patterns,replacements,chance in dialect.structure_rules:
        for pattern in patterns:
            for i in range(len(tagged)):
                if not pos_tag_match(tagged,i,pattern):
                    continue
                if random.random() >= chance:
                    continue
                replacement = random.choice(replacements)
                new = tagged[:i]
                for r in replacement:
                    if type(r)==int:
                        new += [tagged[i+r]]
                    else:
                        new += [(r,"?")]
                new += tagged[i+len(pattern):]
                tagged = new
                break

    return [word for word,tag in tagged[1:-1]]


def pos_tag_match(tagged,i,pattern):
    for j,ptag in enumerate(pattern):
        if i+j >= len(tagged):
            return False
        if not bool(re.match("^"+ptag.replace("*",".*")+"$",tagged[i+j][1])):
            return False
    return True
    

def match_phoneme(phons, i, pattern):
    """Match the given pattern from position i in a sequence of phonemes."""
    for j, pfon in enumerate(pattern):
        if i + j >= len(phons):
            return False
        next_phoneme = phons[i + j][0]
        if not next_phoneme:
            return False
        elif pfon == "VOWEL":
            if next_phoneme[0] not in 'AEIOU':
                return False
            continue
        elif pfon == "CONS":
            if next_phoneme[0] in 'AEIOU':
                return False
            continue
        # Match vowel stress digit if exists in pattern otherwise ignore
        elif pfon != (next_phoneme if pfon[-1].isdigit() else match_digits.sub('', next_phoneme)):
            return False

    return True


def substitute(tokens, dialect):
    """Generator producing translated words for given tokens.

    Algorithm:
        1. Try direct word substitution
        2. If (1) fails, try phonetic substitution.
        3. If (2) fails, it's a symbol! Return as is...

    """
    for token in tokens:
        token_lower = token.lower()
        if token_lower in dialect.ignores:
            yield token
            continue
        substitution = replace_random(token_lower, dialect)
        if substitution == token_lower:
            substitution = alter_phonemes(token_lower, dialect)

        yield match_case(substitution, token)


def alter_phonemes(word, dialect, phonetic=False):
    """Apply the dialect's phoneme rules to a word.
    
    If phonetic=True, convert the spelling of the word to a purely phonetic one.
    """
    try:
        phons = pronounce(word)
    except KeyError:
        return word

    logging.debug('Phoneme In=[%s->%s]', word, phons)
    phons = [("START", '')] + phons + [("END", '')]

    for patterns, replacement in dialect.phoneme_rules:
        for pattern in patterns:
            for i in range(len(phons)):
                if match_phoneme(phons,i,pattern):
                    r = [phons[i+rfon] if type(rfon)==int else Phoneme(phoneme=rfon, grapheme=grapheme(rfon)) for rfon in replacement]
                    phons = phons[:i] + r + phons[i+len(pattern):]

    logging.debug('Phoneme Out=[%s->%s]', word, phons)
    return "".join((p.grapheme if not phonetic else grapheme(p.phoneme)) for p in phons[1:-1])


def replace_random(word,dialect):
    """Replace given word with a random alternative from given dialect.

    If a replacement word does not exist, return the original word.

    """
    for patterns, replacements in dialect.word_rules:
        if word in patterns:
            return random.choice(replacements)

    # No replacement found
    return word


def tokenize(text):
    """Tokenize a block of text into a list of words and symbols.

    Features:
      - Retain newlines.
      - Retain special characters.

    """
    tokens = (wordpunct_tokenize(line) + ['\n'] for line in text.splitlines())
    return list(chain.from_iterable(tokens))[:-1]


def untokenize(tokens):
    """Join a sequence of tokens into a single block of text.

    An attempt is made to respect the location of whitespace in the
    original text.

    """

    def spacer():
        token = tokens.next()
        yield token

        last = token
        for token in tokens:
            if any(c.isalnum() for c in token) and not last.isspace():
                yield ' '
            yield token
            last = token

    return ''.join(list(spacer()))


def match_case(text, match_text):
    """Return text capitalised to match match_text."""
    word_count = len(match_text.split())
    if match_text.istitle() and word_count == 1:
        return text.capitalize()
    elif match_text.istitle():
        return text.title()
    elif match_text[0].isupper():
        return text.capitalize()
    else:
        return text


def main():
    """Entry point to run the standalone translator on a file or on stdin."""
    import sys
    f = sys.stdin if len(sys.argv) == 1 else open(sys.argv[1])
    print(translate(f.read()))


if __name__ == '__main__':
    main()
