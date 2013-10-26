from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')

import sys
import argparse
import configparser
import logging
import locale
from wsgiref.simple_server import make_server

from mancify import MancifyWsgiApp


# Use the user's default locale instead of C
locale.setlocale(locale.LC_ALL, '')

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


class MancifyConsoleApp(object):
    def __init__(self):
        super(MancifyConsoleApp, self).__init__()
        self.parser = argparse.ArgumentParser(
            description = self.__doc__,
            argument_default=argparse.SUPPRESS)
        self.parser.set_defaults(log_level=logging.WARNING)
        self.parser.add_argument('--version', action='version',
            version=__version__)
        self.parser.add_argument(
            '-q', '--quiet', dest='log_level', action='store_const',
            const=logging.ERROR, help='produce less console output')
        self.parser.add_argument(
            '-v', '--verbose', dest='log_level', action='store_const',
            const=logging.INFO, help='produce more console output')
        self.parser.add_argument(
            '-l', '--log-file', dest='log_file', metavar='FILE', default=None,
            help='log messages to the specified file')
        self.parser.add_argument(
            '-P', '--pdb', dest='debug', action='store_true', default=False,
            help='run under PuDB/PDB (debug mode)')
        self.parser.add_argument(
            '-L', '--listen', dest='listen', action='store',
            default='0.0.0.0:%d' % (8000 if os.geteuid() else 80),
            metavar='HOST[:PORT]', type=interface,
            help='the address and port of the interface the web-server will '
            'listen on. Default: %(default)s')
        self.parser.add_argument(
            '--exec-timeout', dest='exec_timeout', action='store', default=10,
            type=int, help='the timeout for executing commands over SSH')
        self.parser.add_argument(
            '--connect-timeout', dest='connect_timeout', action='store', default=30,
            type=int, help='the timeout for SSH connections')
        self.parser.add_argument(
            '--session-timeout', dest='session_timeout', action='store', default=300,
            type=int, help='the timeout between SSH commands')
        self.parser.add_argument(
            '--clockwork-api-key', dest='clockwork_api_key', action='store',
            default=None, help='your clockwork API key')

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
                return 1

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
        config = configparser.ConfigParser(interpolation=None)
        logging.info('Reading configuration from %s', ', '.join(conf_files))
        conf_read = config.read(conf_files)
        if conf_args.config and conf_args.config not in conf_read:
            self.parser.error('unable to read %s', conf_args.confg)
        if conf_read:
            section = 'mancify'
            if not section in config:
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
                if key in config[section]
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
        app = MancifyWsgiApp(**vars(args))
        httpd = make_server(args.listen[0], args.listen[1], app)
        logging.info('Listening on %s:%s' % (args.listen[0], args.listen[1]))
        httpd.serve_forever()
        return 0


main = MancifyConsoleApp()

if __name__ == '__main__':
    sys.exit(main())

