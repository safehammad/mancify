from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')

import sys
import os
import re
import argparse
import ConfigParser
import logging
import locale
import curses
import curses.ascii
import curses.textpad
from itertools import izip_longest
from wsgiref.simple_server import make_server

from mancify import __version__
from mancify.translator import translate
from mancify.wsgi import MancifyWsgiApp


# Use the user's default locale instead of C
locale.setlocale(locale.LC_ALL, '')
ENCODING = locale.getpreferredencoding()

# Set up a console logging handler which just prints messages to stderr without
# any other adornments. This will be used for logging messages sent before we
# "properly" configure logging according to the user's preferences
_CONSOLE = logging.StreamHandler(sys.stderr)
_CONSOLE.setFormatter(logging.Formatter('%(message)s'))
_CONSOLE.setLevel(logging.DEBUG)
logging.getLogger().addHandler(_CONSOLE)

# Determine the location of the current module on the filesystem
HERE = os.path.abspath(os.path.dirname(__file__))


def interface(s):
    """
    Parses a string containing a host[:port] specification.
    """
    if not s:
        return None
    if ':' in s:
        host, port = s.split(':', 1)
        if not host:
            host = '0.0.0.0'
        if port.isdigit():
            port = int(port)
    else:
        host = s
        port = 80
    return (host, port)


class BaseConsoleApp(object):
    def __init__(self):
        super(BaseConsoleApp, self).__init__()
        self.parser = argparse.ArgumentParser(
            description = self.__doc__,
            argument_default=argparse.SUPPRESS)
        self.parser.set_defaults(log_level=logging.WARNING)
        self.parser.add_argument('--version', action='version',
            version=__version__)
        self.parser.add_argument(
            '-c', '--config', dest='config', action='store',
            help='specify the configuration file to load')
        self.parser.add_argument(
            '-l', '--log-file', dest='log_file', metavar='FILE', default=None,
            help='log messages to the specified file')
        self.parser.add_argument(
            '-P', '--pdb', dest='debug', action='store_true', default=False,
            help='run under PuDB/PDB (debug mode)')

    def __call__(self, args=None):
        if args is None:
            args = sys.argv[1:]
        args = self.read_configuration(args)
        args = self.parser.parse_args(args)
        self.configure_logging(args)
        if args.debug:
            try:
                import pudb
            except ImportError:
                pudb = None
                import pdb
            return (pudb or pdb).runcall(self.main, args)
        else:
            try:
                return self.main(args) or 0
            except Exception as e:
                logging.error(str(e))
                raise

    def read_configuration(self, args):
        # Parse the --config argument only
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-c', '--config', dest='config', action='store')
        conf_args, args = parser.parse_known_args(args)
        conf_files = [
            '/etc/mancify.ini',                   # system wide config
            '/usr/local/etc/mancify.ini',         # alternate system config
            os.path.expanduser('~/.mancify.ini'), # user config
            ]
        if conf_args.config:
            conf_files.append(conf_args.config)
        config = ConfigParser.ConfigParser()
        logging.info('Reading configuration from %s', ', '.join(conf_files))
        conf_read = config.read(conf_files)
        if conf_args.config and conf_args.config not in conf_read:
            self.parser.error('unable to read %s', conf_args.confg)
        if conf_read:
            section = 'mancify'
            if not section in config.sections():
                self.parser.error(
                    'unable to locate [%s] section in configuration' % section)
            self.parser.set_defaults(**{
                key:
                config.getboolean(section, key)
                if key in ('pdb',) else
                config.get(section, key)
                for key in (
                    'pdb',
                    'log_file',
                    'listen',
                    'exec_timeout',
                    'connect_timeout',
                    'session_timeout',
                    'clockwork_api_key',
                    )
                if config.has_option(section, key)
                })
        return args

    def configure_logging(self, args):
        _CONSOLE.setLevel(args.log_level)
        if args.log_file:
            log_file = logging.FileHandler(args.log_file)
            log_file.setFormatter(
                logging.Formatter('%(asctime)s, %(levelname)s, %(message)s'))
            log_file.setLevel(logging.DEBUG)
            logging.getLogger().addHandler(log_file)
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def main(self, args):
        raise NotImplementedError


class MancifyCursesApp(BaseConsoleApp):
    def __init__(self):
        super(MancifyCursesApp, self).__init__()

    def main(self, args):
        translate('')
        curses.wrapper(self.event_loop)

    def event_loop(self, screen):
        y, x = screen.getmaxyx()
        in_win = screen.subwin(y // 2, x, 0, 0)
        out_win = screen.subwin(y // 2 - 1, x, y // 2 + 1, 0)
        in_box = curses.textpad.Textbox(in_win)
        old_content = []
        new_content = []
        content = []
        while True:
            c = in_win.getch()
            in_box.do_command(c)
            pos = in_win.getyx()
            old_content = content
            new_content = [(word, None) for word in re.split(r'(\s+)', in_box.gather().replace('\n', ' '))]
            content = []
            for (old_word, new_word) in izip_longest(old_content, new_content):
                if new_word is None:
                    pass
                elif (old_word is None) or (old_word[0] != new_word[0]):
                    if not new_word[0]:
                        pass
                    elif re.match('\s+', new_word[0]):
                        content.append((new_word[0], new_word[0]))
                    else:
                        content.append((new_word[0], translate(new_word[0])))
                else:
                    content.append(old_word)
            out_win.clear()
            out_win.addstr(0, 0, ''.join(t for (w, t) in content))
            in_win.move(*pos)
            out_win.refresh()


class MancifyConsoleApp(BaseConsoleApp):
    def __init__(self):
        super(MancifyConsoleApp, self).__init__()
        self.parser.add_argument(
            '-q', '--quiet', dest='log_level', action='store_const',
            const=logging.ERROR, help='produce less console output')
        self.parser.add_argument(
            '-v', '--verbose', dest='log_level', action='store_const',
            const=logging.INFO, help='produce more console output')
        self.parser.add_argument(
            '-L', '--listen', dest='listen', action='store',
            default='0.0.0.0:%d' % (8000 if os.geteuid() else 80),
            metavar='HOST[:PORT]', type=interface,
            help='the address and port of the interface the web-server will '
            'listen on. Default: %(default)s')
        self.parser.add_argument(
            '--exec-timeout', dest='exec_timeout', action='store', default=10,
            metavar='SECS', type=int,
            help='the timeout for executing commands over SSH')
        self.parser.add_argument(
            '--connect-timeout', dest='connect_timeout', action='store',
            default=30, metavar='SECS', type=int,
            help='the timeout for SSH connections')
        self.parser.add_argument(
            '--session-timeout', dest='session_timeout', action='store',
            default=300, metavar='SECS', type=int,
            help='the timeout between SSH commands')
        self.parser.add_argument(
            '--output-limit', dest='output_limit', action='store',
            default=1024, metavar='BYTES', type=int,
            help='the maximum size of output to permit per command')
        self.parser.add_argument(
            '--clockwork-api-key', dest='clockwork_api_key', action='store',
            metavar='KEY', default=None,
            help='your clockwork API key')

    def get_app(self, ini_path=None):
        args = []
        if ini_path:
            args = ['-c', ini_path]
        args = self.read_configuration(args)
        args = self.parser.parse_args(args)
        self.configure_logging(args)
        return MancifyWsgiApp(**vars(args))

    def main(self, args):
        app = MancifyWsgiApp(**vars(args))
        try:
            httpd = make_server(args.listen[0], args.listen[1], app)
            logging.info('Listening on %s:%s' % (args.listen[0], args.listen[1]))
            httpd.serve_forever()
        finally:
            app.close()
        return 0


curses_main = MancifyCursesApp()
serve_main = MancifyConsoleApp()

if __name__ == '__main__':
    sys.exit(main())

