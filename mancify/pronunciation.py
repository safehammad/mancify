from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
)

import re
from collections import namedtuple
from itertools import chain

from nltk.corpus import cmudict


# The CMU pronunciation dictionary
phoneme_dict = cmudict.dict()


# Regex match a digit
re_digits = re.compile(r'\d')


# A phoneme with associated word fragment
Phoneme = namedtuple('Phoneme', 'phoneme, spelling')


# The most intuitive English spelling for a given phoneme
phoneme_reprs = {
    "AA":   "o",    # 'o' as in 'odd'
    "AE":   "a",    # 'a' as in 'at'
    "AH":   "uh",   # 'u' as in 'hut'
    "AO":   "oar",  # 'augh' as in 'caught'
    "AW":   "ow",   # 'ow' as in 'cow'
    "AY":   'iy',   # 'i' as in 'hide'
    "B":    'b',    # 'b' as in 'bee'
    "CH":   'ch',   # 'ch' as in 'cheese'
    "D":    'd',    # 'd' as in 'dog'
    "DH":   'th',   # 'th' as in 'thee'
    "EH":   'e',    # 'e' as in 'Ed'
    "ER":   'ur',   # 'ur' as in 'hurt'
    "EY":   'ey',   # 'a' as in 'ate'
    "F":    'f',    # 'f' as in 'fee'
    "G":    'g',    # 'g' as in 'green'
    "HH":   'h',    # 'h' as in 'house'
    "IH":   'i',    # 'i' as in 'it'
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
    "UH":   'u',    # 'oo' as in 'hood'
    "UW":   'oo',   # 'wo' as in 'two'
    "V":    'v',    # 'v' as in 'vee'
    "W":    'w',    # 'w' as in 'we'
    "Y":    'y',    # 'y' as in 'yeild'
    "Z":    'z',    # 'z' as in 'zee'
    "ZH":   'z',    # 'z' as in 'seizure'
    "'":    "'",    # glottal stop
}


# For each phoneme, a list of spellings for English
# consonants which might give rise to that phoneme.
phoneme_sounds = {
    "B":    ['b'],                  # 'b' as in 'bee'
    "CH":   ['ch', 'tch'],          # 'ch' as in 'cheese'
    "D":    ['d'],                  # 'd' as in 'dog'
    "DH":   ['th'],                 # 'th' as in 'thee'
    "F":    ['f', 'ph', 'gh'],      # 'f' as in 'fee'
    "G":    ['g'],                  # 'g' as in 'green'
    "HH":   ['h'],                  # 'h' as in 'house'
    "JH":   ['dg', 'g', 'j'],       # 'g' as in 'gee'
    "K":    ['c', 'ck', 'cq',       # 'k' as in 'key'
             'k', 'q', 'x'],
    "L":    ['l'],                  # 'l' as in 'lee'
    "M":    ['m'],                  # 'm' as in 'me'
    "N":    ['n'],                  # 'kn' as in 'knee'
    "NG":   ['ng'],                 # 'ng' as in 'ping'
    "P":    ['p'],                  # 'p' as in 'pee'
    "R":    ['r'],                  # 'r' as in 'read'
    "S":    ['c', 's'],             # 's' as in 'sea'
    "SH":   ['ch', 'sh', 'ti'],     # 'sh' as in 'she'
    "T":    ['t'],                  # 't' as in 'tea'
    "TH":   ['th'],                 # 'th' as in 'theta'
    "V":    ['v'],                  # 'v' as in 'vee'
    "W":    ['u', 'w'],             # 'w' as in 'we'
    "Y":    ['i', 'y'],             # 'y' as in 'yield'
    "Z":    ['s', 'z'],             # 'z' as in 'zee'
    "ZH":   ['g', 'j', 'z'],        # 'z' as in 'seizure'
    "'":    ["'"],                  # glottal stop
}


def spell(phoneme):
    """Return the most intuitive spelling for the given phoneme.
    
    Return the empty string if the given phoneme is not recognised.

    """
    return phoneme_reprs.get(phoneme, '')


def partition_score(partition):
    """For a 3-tuple of strings (a, b, c) provide a lower score for a smaller a and larger b."""
    prefix, consonant, suffix = partition
    return len(prefix), -len(consonant)


def match_consonant(text, consonant_phoneme):
    """Find the best matching consonant given a consonant phoneme.
    
    Return partitioned text as a 3-tuple i.e. (prefix, consonant, suffix).

    >>> match_consonant('observe', 'Z')
    ('ob', 's', 'erve')
    
    Note that the best consonant might be a diphthong or doubled letter.
    For example, "th", "ng", "tch", "tt".

    """
    partitions = [text.partition(consonant)
                  for consonant in phoneme_sounds[consonant_phoneme]
                  if consonant in text]

    if not partitions:
        return '', '', text

    prefix, consonant, suffix = min(partitions, key=partition_score)
    # Check for doubled consonants e.g. 's' in assert
    if suffix.startswith(consonant):
        return prefix, consonant + consonant, suffix[1:]
    else:
        return prefix, consonant, suffix


def distribute_letters(phonemes, letters):
    """Distribute letters across phonemes.

    For example, where ian = ['IY1', 'AH0', 'N']:

    >>> distribute_letters(['IY1', 'AH0'], 'ia')
    [('IY1', 'i'), ('AH0', 'a')]
    
    """
    step = int(round(len(letters) / len(phonemes)))
    return [Phoneme(phoneme=phoneme, spelling=letters[i * step: (i + 1) * step])
             for i, phoneme in enumerate(phonemes)]


def pronounce(word):
    """Return the pronunciation of a word whilst maintaining the relationship between
    the original letters of the word and the resulting phonemes. The function attempts
    to retain the association by pinning consonant phonemes to the most likely consonant
    letters in the word and distributing the remaining letters to the vowel phonemes.

    Returns a list of 2-tuples of type Phoneme: [(phoneme, spelling), ...]

    For example:
    >>> pronounce('assert')
    [('AH0', u'a'), ('S', u'ss'), ('ER1', u'er'), ('T', u't')]

    Raises KeyError if the word is not recognised.
    """
    remainder = word.lower()
    vowel_phonemes = []
    result = []
    pronunciation = [re_digits.sub('', p) for p in phoneme_dict[word.lower()][0]]
    for phoneme in pronunciation:
        if phoneme[0] in 'AEIOU':
            vowel_phonemes.append(phoneme)
            continue

        vowel, consonant, remainder = match_consonant(remainder, phoneme)
        if vowel_phonemes:
            result.extend(distribute_letters(vowel_phonemes, vowel))
            vowel_phonemes = []
        elif vowel:
            result.append(Phoneme(phoneme='', spelling=vowel))
        result.append(Phoneme(phoneme=phoneme, spelling=consonant))

        if not remainder:
            break

    if vowel_phonemes:
        result.extend(distribute_letters(vowel_phonemes, remainder))
    elif remainder:
        result.append(Phoneme(phoneme='', spelling=remainder))

    return result
