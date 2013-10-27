from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')

import re
import logging
import socket
from datetime import datetime

from paramiko import SSHClient, SSHException, AutoAddPolicy

from mancify import translator
from mancify.dialects import manc, normal


class MancifySSHSession(object):
    connect_re = re.compile(r'ssh +(?P<username>[^@ ]+)@(?P<hostname>[^ ]+) +(?P<password>[^ ]+)( +(?P<dialect>.*))?')
    dialects = {
        'manc':   manc,
        'normal': normal,
    }

    def __init__(
            self, sms, sender, recipient, connect_timeout=30, exec_timeout=10):
        self.sms = sms
        self.sender = sender
        self.recipient = recipient
        self.connect_timeout = connect_timeout
        self.exec_timeout = exec_timeout
        self.timestamp = None
        self.hostname = None
        self.client = None
        self.dialect = None

    def open(self, content):
        match = self.connect_re.match(content)
        if not match:
            self.send(
                'Invalid connection request. Please send '
                'ssh username@host password [dialect]')
        self.hostname = match.group('hostname')
        username = match.group('username')
        password = match.group('password')
        self.dialect = self.dialects.get(match.group('dialect'), manc)
        logging.info('Opening connection to %s for %s', self.hostname, self.sender)
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(
            self.hostname, username=username, password=password,
            timeout=self.connect_timeout)
        self.send('Connected to %s' % self.hostname)

    def close(self):
        logging.info('Closing connection to %s for %s', self.hostname, self.sender)
        session.close()
        self.hostname = None
        self.client = None
        self.dialect = None
        self.timestamp = None
        self.send('Closed connection to %s' % self.hostname)

    def execute(self, content):
        if not self.client:
            self.open(content)
        elif content == '^D' or content == 'logout':
            self.close()
        else:
            logging.debug('Executing %s for %s', content, self.recipient)
            stdin, stdout, stderr = self.client.exec_command(
                    content, timeout=self.exec_timeout)
            out = stdout.read()
            err = stderr.read()
            if out and err:
                msg = 'out:%s\nerr:%s' % (out, err)
            elif out:
                msg = out
            elif err:
                msg = err
            else:
                msg = "There's nothing to output!"
            self.send(msg)

    def send(self, content):
        self.sms.send(
            self.sender, self.recipient,
            translator.translate(content, self.dialect))

