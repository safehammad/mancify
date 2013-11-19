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
            ('assert', [('AH0', 'a'), ('S', 'ss'), ('ER1', 'er'), ('T', 't')]),
            ('shott', [('SH', 'sh'), ('AA1', 'o'), ('T', 'tt')]),
            ('accept', [('AE0', 'a'), ('K', 'c'), ('S', 'c'), ('EH1', 'e'), ('P', 'p'), ('T', 't')]),
            ('session', [('S', 's'), ('EH1', 'e'), ('SH', 'ssi'), ('AH0', 'o'), ('N', 'n')]),
        ]
        self._test_pronunciations(tests)

    def testDoubleConsonant(self):
        tests = [
            ('acknowledge', [('AE0', 'a'), ('K', 'ck'), ('N', 'n'), ('AA1', 'ow'), ('L', 'l'), ('IH0', 'e'), ('JH', 'dg'), ('', 'e')]),
        ]
        self._test_pronunciations(tests)

    def testConsonantDiphthong(self):
        tests = [
            ('sphere', [('S', 's'), ('F', 'ph'), ('IH1', 'e'), ('R', 'r'), ('', 'e')]),
        ]
        self._test_pronunciations(tests)

    def testQu(self):
        tests = [
            ('queen', [('K', 'q'), ('W', 'u'), ('IY1', 'ee'), ('N', 'n')]),
            ('ye', [('Y', 'y'), ('IY1', 'e')]),
        ]
        self._test_pronunciations(tests)

    # VOWEL TESTS

    def testDoubleVowel(self):
        tests = [
            ('ian', [('IY1', 'i'), ('AH0', 'a'), ('N', 'n')]),
            ('fluid', [('F', 'f'), ('L', 'l'), ('UW1', 'u'), ('AH0', 'i'), ('D', 'd')]),
        ]
        self._test_pronunciations(tests)

    def testVowelWithConsonantLetters(self):
        tests = [
            ('caught', [('K', 'c'), ('AA1', 'augh'), ('T', 't')]),
            ('through', [('TH', 'th'), ('R', 'r'), ('UW1', 'ough')]),
            ('cough', [('K', 'c'), ('AA1', 'ou'), ('F', 'gh')]),  # Distinguish gh as 'f'
        ]
        self._test_pronunciations(tests)

    def testSilentE(self):
        tests = [
            ('like', [('L', 'l'), ('AY1', 'i'), ('K', 'k'), ('', 'e')]),
            ('home', [('HH', 'h'), ('OW1', 'o'), ('M', 'm'), ('', 'e')]),
        ]
        self._test_pronunciations(tests)

    def testInitialAndFinalVowel(self):
        tests = [
            ('auntie', [('AE1', 'au'), ('N', 'n'), ('T', 't'), ('IY0', 'ie')]),
            ('attach', [('AH0', 'a'), ('T', 'tt'), ('AE1', 'a'), ('CH', 'ch')]),
            ('attache', [('AE2', 'a'), ('T', 'tt'), ('AH0', 'a'), ('SH', 'ch'), ('EY1', 'e')]),
        ]
        self._test_pronunciations(tests)

    # PHONEME / SPELLING COVERAGE
    def testPhonemeCoverage(self):
        """Spellings for all phonemes should be covered here."""
        tests = [
            ('beef', [('B', 'b'), ('IY1', 'ee'), ('F', 'f')]),
            ('cheese', [('CH', 'ch'), ('IY1', 'ee'), ('Z', 's'), ('', 'e')]),
            ('hitch', [('HH', 'h'), ('IH1', 'i'), ('CH', 'tch')]),
            ('wind', [('W', 'w'), ('AY1', 'i'), ('N', 'n'), ('D', 'd')]),
            ('the', [('DH', 'th'), ('AH0', 'e')]),
            ('phone', [('F', 'ph'), ('OW1', 'o'), ('N', 'n'), ('', 'e')]),
            ('rough', [('R', 'r'), ('AH1', 'ou'), ('F', 'gh')]),
            ('garage', [('G', 'g'), ('ER0', 'ar'), ('AA1', 'a'), ('ZH', 'g'), ('', 'e')]),
            ('edge', [('EH1', 'e'), ('JH', 'dg'), ('', 'e')]),
            ('agile', [('AE1', 'a'), ('JH', 'g'), ('AH0', 'i'), ('L', 'l'), ('', 'e')]),
            ('jack', [('JH', 'j'), ('AE1', 'a'), ('K', 'ck')]),
            ('ping', [('P', 'p'), ('IH1', 'i'), ('NG', 'ng')]),
            ('sun', [('S', 's'), ('AH1', 'u'), ('N', 'n')]),
            ('piece', [('P', 'p'), ('IY1', 'ie'), ('S', 'c'), ('', 'e')]),
            ('shot', [('SH', 'sh'), ('AA1', 'o'), ('T', 't')]),
            ('accession', [('AH0', 'a'), ('K', 'c'), ('S', 'c'), ('EH1', 'e'), ('SH', 'ssi'), ('AH0', 'o'), ('N', 'n')]),
            ('nation', [('N', 'n'), ('EY1', 'a'), ('SH', 'ti'), ('AH0', 'o'), ('N', 'n')]),
            ('attache', [('AE2', 'a'), ('T', 'tt'), ('AH0', 'a'), ('SH', 'ch'), ('EY1', 'e')]),
            ('thick', [('TH', 'th'), ('IH1', 'i'), ('K', 'ck')]),
            ('vat', [('V', 'v'), ('AE1', 'a'), ('T', 't')]),
            ('aqua', [('AE1', 'a'), ('K', 'q'), ('W', 'u'), ('AH0', 'a')]),
            ('ye', [('Y', 'y'), ('IY1', 'e')]),
            ('uniform', [('Y', 'u'), ('UW1', ''), ('N', 'n'), ('AH0', 'i'), ('F', 'f'), ('AO2', 'o'), ('R', 'r'), ('M', 'm')]),
            ('spaniel', [('S', 's'), ('P', 'p'), ('AE1', 'a'), ('N', 'n'), ('Y', 'i'), ('AH0', 'e'), ('L', 'l')]),
            ('zoo', [('Z', 'z'), ('UW1', 'oo')]),
            ('phase', [('F', 'ph'), ('EY1', 'a'), ('Z', 's'), ('', 'e')]),
            ('seizure', [('S', 's'), ('IY1', 'ei'), ('ZH', 'z'), ('ER0', 'ure')]),
            ('jacque', [('ZH', 'j'), ('EY1', 'a'), ('K', 'cq'), ('', 'ue')]),
            ('occasion', [('AH0', 'o'), ('K', 'cc'), ('EY1', 'a'), ('ZH', 'si'), ('AH0', 'o'), ('N', 'n')]),
        ]
        self._test_pronunciations(tests)


class TestPhonemeMatch(unittest.TestCase):
    def setUp(self):
        # Pronunciation of "hat" with start and end markers
        self.hat = [('START', ''), ('HH', 'h'), ('AE1', 'a'), ('T', 't'), ('END', '')]

    def testMatchLocation(self):
        """Check that a matching phoneme is found only in the correct location."""
        self.assertTrue(translator.match_phoneme(self.hat, 1, ['HH']))
        self.assertFalse(translator.match_phoneme(self.hat, 2, ['HH']))

    def testMatchVowelPhonemeNoStress(self):
        """A vowel pattern with no stress should match a vowel with any stress."""
        self.assertTrue(translator.match_phoneme([('AE0', 'a')], 0, ['AE']))
        self.assertTrue(translator.match_phoneme([('AE1', 'a')], 0, ['AE']))
        self.assertTrue(translator.match_phoneme([('AE2', 'a')], 0, ['AE']))

    def testMatchVowelPhomemeWithStress(self):
        """A vowel pattern with stress should only match a vowel with same stress."""
        self.assertFalse(translator.match_phoneme([('AE0', 'a')], 0, ['AE1']))
        self.assertTrue(translator.match_phoneme([('AE1', 'a')], 0, ['AE1']))
        self.assertFalse(translator.match_phoneme([('AE2', 'a')], 0, ['AE1']))

    def testMatchVowelMarker(self):
        """Vowel marker should match any vowel and no consonant."""
        self.assertFalse(translator.match_phoneme(self.hat, 1, ['VOWEL']))
        self.assertTrue(translator.match_phoneme(self.hat, 2, ['VOWEL']))

    def testMatchConsonantMarker(self):
        """Consonant marker should match any consonant and no vowel."""
        self.assertTrue(translator.match_phoneme(self.hat, 1, ['CONS']))
        self.assertFalse(translator.match_phoneme(self.hat, 2, ['CONS']))
        self.assertTrue(translator.match_phoneme(self.hat, 3, ['CONS']))

    def testMatchStart(self):
        self.assertTrue(translator.match_phoneme(self.hat, 0, ['START']))
        self.assertFalse(translator.match_phoneme(self.hat, 1, ['START']))

    def testMatchEnd(self):
        self.assertTrue(translator.match_phoneme(self.hat, 4, ['END']))
        self.assertFalse(translator.match_phoneme(self.hat, 3, ['END']))
