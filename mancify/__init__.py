# Project meta-data

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
    'sms',
    'ssh',
    'silly',
    ]

__requires__ = [
    'numpy<2.0dev',
    'paramiko<2.0dev',
    'clockwork<2.0dev',
    'webob<2.0dev',
    'wheezy.routing<1.0dev',
    'nltk==2.0.4',
    ]

__extra_requires__ = {
    'doc': ['sphinx'],
    }

__entry_points__ = {
    'console_scripts': [
        'mancify = mancify.terminal:main',
        ],
    }

