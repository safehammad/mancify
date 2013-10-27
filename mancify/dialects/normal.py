from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')


class AllSet(object):
    def __contains__(self, item):
        return True

ignores = AllSet()
word_rules = []
phoneme_rules = []
structure_rules = []
