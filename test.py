import unittest

import translator
import manc


class TestMancify(unittest.TestCase):
    def testTranslate(self):
        sample = 'This is a line. &This line ^has some symbols.\n This is the next line.'
        expected = ['This', 'is', 'a', 'line', '.', '&', 'This', 'line', '^', 'has', 'some', 'symbols', '.', '\n', 'This', 'is', 'the', 'next', 'line', '.']
        self.assertItemsEqual(expected, translator.translate(sample))

    def testReplace(self):
        self.assertTrue(manc.replace_random('bad') in ['shit', 'knackered', 'naff'])
        self.assertTrue(manc.replace_random('poor') in ['shit', 'knackered', 'naff'])
