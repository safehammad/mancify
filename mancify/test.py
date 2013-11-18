import unittest
from itertools import chain

from . import translator
from .pronunciation import pronounce
from .dialects import manc


class TestMancify(unittest.TestCase):
    def testTokenize(self):
        text = 'A line. &A line ^with symbols.\nThe next line.\nAnother line.'
        expected = ['A', 'line', '.', '&', 'A', 'line', '^', 'with', 'symbols', '.', '\n', 'The', 'next', 'line', '.', '\n', 'Another', 'line', '.']
        actual = translator.tokenize(text)
        self.assertItemsEqual(expected, actual)

    def testTranslateWord(self):
        replacements = ["naff","shit","knackered","buggered","pants","pear-shaped","tits up",
                        "ragged","devilled","out of order","bang out of order","biz","kippered",
                        "bobbins"]
        self.assertIn(translator.translate('bad'), replacements)
        self.assertIn(translator.translate('poor'), replacements)

    def testSpacer(self):
        # Check whitespace is maintained
        text = 'This is a very, very good test!\nLine two. And again!'
        tokens = translator.tokenize(text)
        self.assertEqual(text, translator.untokenize(chain(tokens)))

    def testSpacerNonAlnum(self):
        # Check whitespace is maintained with non alphanumeric in token
        tokens = ['This', 'is', 'a', 'pseudo-test']
        self.assertEqual(' '.join(tokens), translator.untokenize(chain(tokens)))

    def testMatchCase(self):
        self.assertEqual('how do', translator.match_case('how do', 'sample'))
        self.assertEqual('How do', translator.match_case('how do', 'Sample'))
        self.assertEqual('How do', translator.match_case('how do', 'Sample text'))
        self.assertEqual('How Do', translator.match_case('how do', 'Sample Text'))


class TestPronunciation(unittest.TestCase):

    def _test_pronunciations(self, tests):
        for word, expected in tests:
            self.assertListEqual(expected, pronounce(word))

    # CONSONANT TESTS

    def testRepeatedConsonant(self):
        tests = [
            ('assert', [('AH', 'a'), ('S', 'ss'), ('ER', 'er'), ('T', 't')]),
            ('shott', [('SH', 'sh'), ('AA', 'o'), ('T', 'tt')]),
            ('accept', [('AE', 'a'), ('K', 'c'), ('S', 'c'), ('EH', 'e'), ('P', 'p'), ('T', 't')]),
            ('session', [('S', 's'), ('EH', 'e'), ('SH', 'ss'), ('AH', 'io'), ('N', 'n')]),
        ]
        self._test_pronunciations(tests)

    def testDoubleConsonant(self):
        tests = [
            ('acknowledge', [('AE', 'a'), ('K', 'ck'), ('N', 'n'), ('AA', 'ow'), ('L', 'l'), ('IH', 'e'), ('JH', 'dg'), ('', 'e')]),
        ]
        self._test_pronunciations(tests)

    def testConsonantDiphthong(self):
        tests = [
            ('sphere', [('S', 's'), ('F', 'ph'), ('IH', 'e'), ('R', 'r'), ('', 'e')]),
        ]
        self._test_pronunciations(tests)

    def testQu(self):
        tests = [
            ('queen', [('K', 'q'), ('W', 'u'), ('IY', 'ee'), ('N', 'n')]), ('ye', [('Y', 'y'), ('IY', 'e')]),
        ]
        self._test_pronunciations(tests)

    # VOWEL TESTS

    def testDoubleVowel(self):
        tests = [
            ('ian', [('IY', 'i'), ('AH', 'a'), ('N', 'n')]),
            ('fluid', [('F', 'f'), ('L', 'l'), ('UW', 'u'), ('AH', 'i'), ('D', 'd')]),
        ]
        self._test_pronunciations(tests)

    def testVowelWithConsonantLetters(self):
        tests = [
            ('caught', [('K', 'c'), ('AA', 'augh'), ('T', 't')]),
            ('through', [('TH', 'th'), ('R', 'r'), ('UW', 'ough')]),
            ('cough', [('K', 'c'), ('AA', 'ou'), ('F', 'gh')]),  # Distinguish gh as 'f'
        ]
        self._test_pronunciations(tests)

    def testSilentE(self):
        tests = [
            ('like', [('L', 'l'), ('AY', 'i'), ('K', 'k'), ('', 'e')]),
            ('home', [('HH', 'h'), ('OW', 'o'), ('M', 'm'), ('', 'e')]),
        ]
        self._test_pronunciations(tests)

    def testInitialAndFinalVowel(self):
        tests = [
            ('auntie', [('AE', 'au'), ('N', 'n'), ('T', 't'), ('IY', 'ie')]),
            ('attach', [('AH', 'a'), ('T', 'tt'), ('AE', 'a'), ('CH', 'ch')]),
            ('attache', [('AE', 'a'), ('T', 'tt'), ('AH', 'a'), ('SH', 'ch'), ('EY', 'e')]),
        ]
        self._test_pronunciations(tests)

    # PHONEME / SPELLING COVERAGE
    def testPhonemeCoverage(self):
        """Spellings for all phonemes should be covered here."""
        tests = [
            ('beef', [('B', 'b'), ('IY', 'ee'), ('F', 'f')]),
            ('cheese', [('CH', 'ch'), ('IY', 'ee'), ('Z', 's'), ('', 'e')]),
            ('hitch', [('HH', 'h'), ('IH', 'i'), ('CH', 'tch')]),
            ('wind', [('W', 'w'), ('AY', 'i'), ('N', 'n'), ('D', 'd')]),
            ('the', [('DH', 'th'), ('AH', 'e')]),
            ('phone', [('F', 'ph'), ('OW', 'o'), ('N', 'n'), ('', 'e')]),
            ('rough', [('R', 'r'), ('AH', 'ou'), ('F', 'gh')]),
            ('garage', [('G', 'g'), ('ER', 'ar'), ('AA', 'a'), ('ZH', 'g'), ('', 'e')]),
            ('edge', [('EH', 'e'), ('JH', 'dg'), ('', 'e')]),
            ('agile', [('AE', 'a'), ('JH', 'g'), ('AH', 'i'), ('L', 'l'), ('', 'e')]),
            ('jack', [('JH', 'j'), ('AE', 'a'), ('K', 'ck')]),
            ('ping', [('P', 'p'), ('IH', 'i'), ('NG', 'ng')]),
            ('sun', [('S', 's'), ('AH', 'u'), ('N', 'n')]),
            ('piece', [('P', 'p'), ('IY', 'ie'), ('S', 'c'), ('', 'e')]),
            ('shot', [('SH', 'sh'), ('AA', 'o'), ('T', 't')]),
            ('accession', [('AH', 'a'), ('K', 'c'), ('S', 'c'), ('EH', 'e'), ('SH', 'ss'), ('AH', 'io'), ('N', 'n')]),
            ('nation', [('N', 'n'), ('EY', 'a'), ('SH', 'ti'), ('AH', 'o'), ('N', 'n')]),
            ('attache', [('AE', 'a'), ('T', 'tt'), ('AH', 'a'), ('SH', 'ch'), ('EY', 'e')]),
            ('thick', [('TH', 'th'), ('IH', 'i'), ('K', 'ck')]),
            ('vat', [('V', 'v'), ('AE', 'a'), ('T', 't')]),
            ('aqua', [('AE', 'a'), ('K', 'q'), ('W', 'u'), ('AH', 'a')]),
            ('ye', [('Y', 'y'), ('IY', 'e')]),
            ('uniform', [('Y', 'u'), ('UW', ''), ('N', 'n'), ('AH', 'i'), ('F', 'f'), ('AO', 'o'), ('R', 'r'), ('M', 'm')]),
            ('spaniel', [('S', 's'), ('P', 'p'), ('AE', 'a'), ('N', 'n'), ('Y', 'i'), ('AH', 'e'), ('L', 'l')]),
            ('zoo', [('Z', 'z'), ('UW', 'oo')]),
            ('phase', [('F', 'ph'), ('EY', 'a'), ('Z', 's'), ('', 'e')]),
            ('seizure', [('S', 's'), ('IY', 'ei'), ('ZH', 'z'), ('ER', 'ure')]),
            ('jacque', [('ZH', 'j'), ('EY', 'a'), ('K', 'cq'), ('', 'ue')]),
            ('occasion', [('AH', 'o'), ('K', 'cc'), ('EY', 'a'), ('ZH', 'si'), ('AH', 'o'), ('N', 'n')]),
        ]
        self._test_pronunciations(tests)
