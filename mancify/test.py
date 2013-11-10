import unittest
from itertools import chain

from . import translator
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
