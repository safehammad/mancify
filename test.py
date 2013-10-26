import unittest

import translator
import manc


class TestMancify(unittest.TestCase):
    def testTranslate(self):
        sample = 'A line. &A line ^with symbols.\nThe next line.\nAnother line.'
        expected = ['A', 'line', '.', '&', 'A', 'line', '^', 'with', 'symbols', '.', '\n', 'The', 'next', 'line', '.', '\n', 'Another', 'line', '.']
        actual = translator.translate(sample)
        self.assertItemsEqual(expected, actual)

    def testReplace(self):
        self.assertTrue(manc.replace_random('bad') in ['shit', 'knackered', 'naff'])
        self.assertTrue(manc.replace_random('poor') in ['shit', 'knackered', 'naff'])
