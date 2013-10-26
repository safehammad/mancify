import unittest

import mancify

SAMPLE = 'This is a line. &This line ^has some symbols.\n This is the next line.'

class TestMancify(unittest.TestCase):
    def testTranslate(self):
        sample = 'This is a line. &This line ^has some symbols.\n This is the next line.'
        expected = ['This', 'is', 'a', 'line', '.', '&', 'This', 'line', '^', 'has', 'some', 'symbols', '.', '\n', 'This', 'is', 'the', 'next', 'line', '.']
        self.assertItemsEqual(expected, mancify.translate(SAMPLE))
