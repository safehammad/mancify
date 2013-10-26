#!/usr/bin/env python3
# vim: set et sw=4 sts=4 fileencoding=utf-8:

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

if sys.version_info[0] == 2:
    if not sys.version_info >= (2, 7):
        raise ValueError('This package requires Python 2.7 or above')
elif sys.version_info[0] == 3:
    raise ValueError('This package does not (yet) work on Python 3.x')
else:
    raise ValueError('What version of Python is this?!')

HERE = os.path.abspath(os.path.dirname(__file__))

# Workaround <http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html>
try:
    import multiprocessing
except ImportError:
    pass

__project__      = 'mancify'
__version__      = '0.1'
__author__       = 'Safe Hammad'
__author_email__ = 'safe@sandacre.com'
__url__          = None
__platforms__    = ['ALL']

__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet',
    ]

__keywords__ = [
    'hack',
    'manchester',
    ]

__requires__ = [
    'paramiko',
    'clockwork',
    'webob',
    'wheezy.routing',
    ]

__extra_requires__ = {
    'doc': ['sphinx'],
    }

__entry_points__ = {
    }


# Add a py.test based "test" command
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--cov', __project__,
            '--cov-report', 'term-missing',
            '--cov-report', 'html',
            '--cov-config', 'coverage.cfg',
            'tests',
            ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def main():
    import io
    with io.open(os.path.join(HERE, 'README.rst'), 'r') as readme:
        setup(
            name                 = __project__,
            version              = __version__,
            description          = __doc__,
            long_description     = readme.read(),
            classifiers          = __classifiers__,
            author               = __author__,
            author_email         = __author_email__,
            #url                  = __url__,
            license              = [
                c.rsplit('::', 1)[1].strip()
                for c in __classifiers__
                if c.startswith('License ::')
                ][0],
            keywords             = ' '.join(__keywords__),
            packages             = ['mancify'],
            package_data         = {},
            include_package_data = True,
            platforms            = __platforms__,
            install_requires     = __requires__,
            extras_require       = __extra_requires__,
            zip_safe             = True,
            entry_points         = __entry_points__,
            tests_require        = ['pytest-cov', 'pytest', 'mock'],
            cmdclass             = {'test': PyTest},
            )

if __name__ == '__main__':
    main()


