import unittest
from itertools import chain

import translator
import manc


class TestMancify(unittest.TestCase):
    def testTokenize(self):
        text = 'A line. &A line ^with symbols.\nThe next line.\nAnother line.'
        expected = ['A', 'line', '.', '&', 'A', 'line', '^', 'with', 'symbols', '.', '\n', 'The', 'next', 'line', '.', '\n', 'Another', 'line', '.']
        actual = translator.tokenize(text)
        self.assertItemsEqual(expected, actual)

    def testTranslateWord(self):
        replacements = ['naff', 'shit', 'knackered', 'buggered', 'pants', 'pear-shaped', 'minging']
        self.assertIn(translator.translate('bad'), replacements)
        self.assertIn(translator.translate('poor'), replacements)

    def translate(self):
        text = 'A line. &A line ^with symbols.\nThe next line.\nAnother line.'
        expected = ['A', 'lain', '.', '&', 'A', 'lain', '^', 'wihth', 'sihmbulz', '.', '\n', 'The', 'nehkst', 'lain', '.', '\n', 'Another', 'lain', '.']
        actual = translator.translate(text)
        self.assertItemsEqual(expected, actual)

    def testSpacer(self):
        # Check whitespace is maintained
        text = 'This is a very, very good test!\nLine two. And again!'
        tokens = translator.tokenize(text)
        self.assertEqual(text, translator.untokenize(chain(tokens)))

    def testSpacerNonAlnum(self):
        # Check whitespace is maintained with non alphanumeric in token
        tokens = ['This', 'is', 'a', 'pseudo-test']
        self.assertEqual(' '.join(tokens), translator.untokenize(chain(tokens)))


