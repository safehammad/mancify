import unittest

import translator
import manc


class TestMancify(unittest.TestCase):
    def testTranslate(self):
        sample = 'A line. &A line ^with symbols.\nThe next line.\nAnother line.'
        expected = ['A', 'lain', '.', '&', 'A', 'lain', '^', 'wihth', 'sihmbulz', '.', '\n', 'The', 'nehkst', 'lain', '.', '\n', 'Another', 'lain', '.']
        actual = translator.translate(sample,manc)
        self.assertItemsEqual(expected, actual)

    def testReplace(self):
        self.assertTrue(translator.replace_random('bad',manc) in ("naff","shit","knackered","buggered","pants","pear-shaped","minging",))
        self.assertTrue(translator.replace_random('poor',manc) in ("naff","shit","knackered","buggered","pants","pear-shaped","minging",))
