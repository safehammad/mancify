from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
)

import re
from collections import namedtuple
from itertools import izip_longest

from nltk.corpus import cmudict


# The CMU pronunciation dictionary
phoneme_dict = cmudict.dict()


# Regex match a digit
match_digits = re.compile(r'\d')


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
    "V":    'v',    # 'v' as in 'vent'
    "W":    'w',    # 'w' as in 'we'
    "Y":    'y',    # 'y' as in 'yield'
    "Z":    'z',    # 'z' as in 'zebra'
    "ZH":   'z',    # 'z' as in 'seizure'
    "'":    "'",    # glottal stop
}


# For each phoneme, a list of spellings for English
# consonants which might give rise to that phoneme.
phoneme_sounds = {
    "B":    ['b'],                  # 'b' as in 'bee'
    "CH":   ['ch',                  # 'ch' as in 'cheese'
             'tch'],                # 'tch' as in 'snatch'
    "D":    ['d'],                  # 'd' as in 'dog'
    "DH":   ['th'],                 # 'th' as in 'thee'
    "F":    ['f',                   # 'f' as in 'fee' 
             'ph',                  # 'ph' as in 'phone'
             'gh'],                 # 'gh' as in 'rough'
    "G":    ['g'],                  # 'g' as in 'green'
    "HH":   ['h'],                  # 'h' as in 'house'
    "JH":   ['dg',                  # 'dg' as in 'bridge'
             'g',                   # 'g' as in 'gee'
             'j'],                  # 'j' as in 'jail'
    "K":    ['c',                   # 'c' as in 'car'
             'ck',                  # 'ck' as in 'attack'
             'cq',                  # 'cq' as in 'acquire'
             'k',                   # 'k' as in 'key'
             'q',                   # 'q' as in 'queen'
             'x'],                  # 'x' as in 'fox'
    "L":    ['l'],                  # 'l' as in 'lee'
    "M":    ['m'],                  # 'm' as in 'me'
    "N":    ['n'],                  # 'kn' as in 'knee'
    "NG":   ['ng'],                 # 'ng' as in 'ping'
    "P":    ['p'],                  # 'p' as in 'pee'
    "R":    ['r'],                  # 'r' as in 'read'
    "S":    ['c',                   # 'c' as in 'care'
             's'],                  # 's' as in 'sea'
    "SH":   ['ch',                  # 'ch' as in 'attache'
             'sh',                  # 'sh' as in 'she'
             't',                   # 't' as in 'nation'
             'ss'],                 # 'ss' as in 'session'
    "T":    ['t'],                  # 't' as in 'tea'
    "TH":   ['th'],                 # 'th' as in 'theta'
    "V":    ['v'],                  # 'v' as in 'vent'
    "W":    ['u',                   # 'u' as in 'queen'
             'w'],                  # 'w' as in 'we'
    "Y":    ['i',                   # 'i' as in 'spaniel'
             'y'],                  # 'y' as in 'yield'
    "Z":    ['s',                   # 's' as in 'cars'
             'z'],                  # 'z' as in 'zebra'
    "ZH":   ['g',                   # 'g' as in 'mirage'
             'j',                   # 'j' as in 'jacque'
             's',                   # 's' as in occasion
             'z'],                  # 'z' as in 'seizure'
    "'":    ["'"],                  # glottal stop
}


def spell(phoneme):
    """Return the most intuitive spelling for the given phoneme.

    For example, for 'S', return 's' rather than the possible 'c'.
    
    Return the empty string if the given phoneme is not recognised.

    """
    return phoneme_reprs.get(phoneme, '')


def partition_score(partition):
    """For a 3-tuple of strings (a, b, c) provide a lower score for a smaller a and larger b."""
    prefix, consonant, suffix = partition
    return len(prefix), -len(consonant)


def match_consonant(text, consonant_phoneme, next_phoneme=None):
    """Find the best matching consonant given a consonant phoneme.

    Return partitioned text as a 3-tuple i.e. (prefix, consonant, suffix). Note that the
    'consonant' might be a diphthong or doubled letter, for example, "th", "ng", "tch", "tt".
    
    The best match will generally be the first possible consonant with the greediest
    number of letters. For example, looking for sound 'T' in 'attach', the first match
    is the first 't', but the greediest acceptable match is 'tt' representing that sound.
     
    >>> match_consonant('attach', 'T')
    (u'a', u'tt', u'ach')
    
    The next_phoneme is optionally given as a look ahead to confirm greediness. For example,
    looking for 'K' in 'accept' where 'S' is the next phoneme, will only return the first 'c'
    because the second 'c' qualifies for representing the following 'S' phoneme:

    >>> match_consonant('accept', 'K', 'S')
    (u'a', u'c', u'cept')

    """
    partitions = [text.partition(consonant)
                  for consonant in phoneme_sounds[consonant_phoneme]
                  if consonant in text]

    if not partitions:
        return '', '', text

    prefix, consonant, suffix = min(partitions, key=partition_score)
    # Check for doubled consonants e.g. 's' in assert.
    # Avoid doubling when second consonant represents a new sound e.g. 'c' in success.
    if suffix.startswith(consonant) and suffix[0] not in phoneme_sounds.get(next_phoneme, []):
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


def phonemes(word):
    """Return a list of phonemes for the given word.""" 
    return [match_digits.sub('', p) for p in phoneme_dict[word.lower()][0]]


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

    # Get phonemes for the given word zipped with same phonemes looking forward one index
    pronunciation = phonemes(word)
    pronunciation2 = iter(pronunciation)
    next(pronunciation2)
    for phoneme, next_phoneme in izip_longest(pronunciation, pronunciation2):
        # 'Collect' vowel sounds until we hit a consonant sound
        if phoneme[0] in 'AEIOU':
            vowel_phonemes.append(phoneme)
            continue

        vowel, consonant, remainder = match_consonant(remainder, phoneme, next_phoneme)
        if vowel_phonemes:
            result.extend(distribute_letters(vowel_phonemes, vowel))
            vowel_phonemes = []
        elif vowel:
            result.append(Phoneme(phoneme='', spelling=vowel))
        result.append(Phoneme(phoneme=phoneme, spelling=consonant))

        if not remainder:
            break

    if vowel_phonemes:
        # Add terminal pronounced vowels e.g. 'ie' in 'auntie'
        result.extend(distribute_letters(vowel_phonemes, remainder))
    elif remainder:
        # Add terminal unpronounced vowels e.g. silent 'e' in 'home'
        result.append(Phoneme(phoneme='', spelling=remainder))

    return result
