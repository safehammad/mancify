from itertools import chain
import random
import re

from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import cmudict

import manc


phoneme_reprs = {
    "AA":   "o",    # 'o' as in 'odd'
    "AE":   "a",    # 'a' as in 'at'
    "AH":   "u",    # 'u' as in 'hut'
    "AO":   "oar",  # 'augh' as in 'caught'
    "AW":   "ow",   # 'ow' as in 'cow'
    "AY":   'ai',   # 'i' as in 'hide'
    "B":    'b',    # 'b' as in 'bee'
    "CH":   'ch',   # 'ch' as in 'cheese'
    "D":    'd',    # 'd' as in 'dog'
    "DH":   'th',   # 'th' as in 'thee'
    "EH":   'eh',   # 'e' as in 'Ed'
    "ER":   'ur',   # 'ur' as in 'hurt'
    "EY":   'ey',   # 'a' as in 'ate'
    "F":    'f',    # 'f' as in 'fee'
    "G":    'g',    # 'g' as in 'green'
    "HH":   'h',    # 'h' as in 'house'
    "IH":   'ih',   # 'i' as in 'it'
    "IY":   'ee',   # 'ea' as in 'eat'
    "JH":   'j',    # 'g' as in 'gee'
    "K":    'k',    # 'k' as in 'key'
    "L":    'l',    # 'l' as in 'lee'
    "M":    'm',    # 'm' as in 'me'
    "N":    'n',    # 'kn' as in 'knee'
    "NG":   'ng',   # 'ng' as in 'ping'
    "OW":   'oh',   # 'oa' as in 'oat'
    "OY":   'oy',   # 'oy' as in 'toy'
    "P":    'p',    # 'p' as in 'pee'
    "R":    'r',    # 'r' as in 'read'
    "S":    's',    # 's' as in 'sea'
    "SH":   'sh',   # 'sh' as in 'she'
    "T":    't',    # 't' as in 'tea'
    "TH":   'th',   # 'th' as in 'theta'
    "UH":   'uh',   # 'oo' as in 'hood'
    "UW":   'oo',   # 'wo' as in 'two'
    "V":    'v',    # 'v' as in 'vee'
    "W":    'w',    # 'w' as in 'we'
    "Y":    'y',    # 'y' as in 'yeild'
    "Z":    'z',    # 'z' as in 'zee'
    "ZH":   'z',    # 'z' as in 'seizure'
}

phoneme_dict = cmudict.dict()

def translate(text, dialect=manc):
    """Translate from plain English to given dialect"""
    tokens = tokenize(text)
    translated = substitute(tokens, dialect)
    return untokenize(translated)


def substitute(tokens, dialect):
    """Generator producing translated words for given tokens.
    
    Algorithm:
        1. Try direct word substitution
        2. If (1) fails, try phonetic substitution.
        3. If (2) fails, it's a symbol! Return as is...

    """
    for token in tokens:
        substitution = replace_random(token,dialect)
        if substitution != token:
            yield substitution
        else:
            yield alter_phonemes(token,dialect)


def alter_phonemes(word,dialect):
    """Write out word phonetically, applying phoneme rules in the 
        process"""
    try:
        phons = phoneme_dict[word][0]
    except KeyError:
        return word
        
    phons = [re.sub("[0-9]","",p) for p in phons]
    phons = ["START"] + phons + ["END"]
        
    for patterns, replacement in dialect.phoneme_rules:
        for pattern in patterns:
            for i in range(len(phons)):
                if phons[i:i+len(pattern)] == pattern:
                    "replacing"
                    phons = phons[:i] + replacement + phons[i+len(pattern):]
                    break
       
    return "".join([phoneme_reprs[p] for p in phons[1:-1]])
        

def replace_random(word,dialect):
    """Replace given word with a random Mancunian alternative.

    If a replacement word does not exist, return the original word.

    """
    for patterns, replacements in dialect.word_rules:
        for pattern in patterns:
            if word == pattern:
                return random.choice(replacements)

    # No replacement found
    return word


def tokenize(text):
    """Turn a block of text and tokenize into a list of words and symbols.

    Features:
      - Retain newlines.
      - Retain special characters.

    """
    lines = (line for line in text.split('\n'))
    tokens = (wordpunct_tokenize(line) + ['\n'] for line in lines)
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
