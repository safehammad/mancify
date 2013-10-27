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

from paramiko import SSHClient, AutoAddPolicy, SSHException
from wheezy.routing import PathRouter, url
from webob import Request, Response, exc
from clockwork import clockwork

from mancify import translator
from mancify.dialects import manc, normal
from mancify.sms import MancifySMSService

# Maximum length of an SMS message (with triple concatenation, the maximum
# permitted under GSM)
SMS_MAX_LENGTH = 459


class MancifyWsgiApp(object):
    connect_re = re.compile(r'ssh +(?P<username>[^@ ]+)@(?P<hostname>[^ ]+) +(?P<password>[^ ]+)( +(?P<dialect>.*))?')
    dialects = {
        "manc":   manc,
        "normal": normal,
    }


    def __init__(self, **kwargs):
        super(MancifyWsgiApp, self).__init__()
        self.sms = MancifySMSService(kwargs['clockwork_api_key'])
        self.exec_timeout = kwargs.get('exec_timeout', 10)
        self.connect_timeout = kwargs.get('connect_timeout', 30)
        self.session_timeout = kwargs.get('session_timeout', 300)
        self.output_limit = kwargs.get('output_limit', 1024)
        self.router = PathRouter()
        self.router.add_routes([
            url('/',    self.do_index),
            url('/ssh', self.do_ssh),
            ])
        self.sessions = {}
        self.messages = set()

    def __call__(self, environ, start_response):
        req = Request(environ)
        try:
            handler, kwargs = self.router.match(req.path_info)
            if handler:
                # XXX Workaround wheezy bug
                if 'route_name' in kwargs:
                    del kwargs['route_name']
                resp = handler(req, **kwargs)
            else:
                self.not_found(req)
        except exc.HTTPException as e:
            # The exception is the response
            resp = e
        return resp(environ, start_response)

    def not_found(self, req):
        raise exc.HTTPNotFound(
            "The resource at %s could not be found" % req.path_info)

    def do_index(self, req):
        resp = Response()
        resp.content_type = b'text/html'
        resp.content_encoding = b'utf-8'
        resp.text = """\
<html>
<head><title>Mancify</title></head>
<body>
<h1>Mancify</h1>
<p>Probably the silliest webapp in the world...</p>
</body>
</html>
"""
        return resp

    def do_ssh(self, req):
        # Check the request has the required parameters
        if not 'msg_id' in req.params:
            raise exc.HTTPBadRequest('Missing msg_id parameter')
        if not 'from' in req.params:
            raise exc.HTTPBadRequest('Missing from parameter')
        if not 'content' in req.params:
            raise exc.HTTPBadRequest('Missing content parameter')
        # If we've seen the message before it's a duplicate. Return 200 OK so
        # the server doesn't keep retrying but otherwise ignore it
        msg_id = req.params['msg_id']
        mobile = req.params['from']
        sender = req.params.get('to')
        content = req.params['content']
        if msg_id in self.messages:
            raise exc.HTTPOk('Message already processed')
        self.messages.add(msg_id)
        # Determine if this is a new session or not
        try:
            if mobile in self.sessions:
                if content == '^D' or content == 'logout':
                    self.ssh_close(mobile, sender)
                else:
                    self.ssh_exec(mobile, content, sender)
            else:
                self.ssh_open(mobile, content, sender)
        except Exception as e:
            msg = str(e)
            if len(msg) > 140:
                msg = msg[:137] + '...'
            self.send(sender, mobile, msg)
        raise exc.HTTPOk('Message processed')

    def ssh_open(self, mobile, content, sender=None):
        match = self.connect_re.match(content)
        if not match:
            raise ValueError(
                'Invalid connection request. Please send '
                'ssh username@hostname password [dialect]')
        hostname = match.group('hostname')
        username = match.group('username')
        password = match.group('password')
        dialect = self.dialects.get(match.group('dialect'), manc)
        logging.info('Opening connection to %s for %s', hostname, username)
        session = SSHClient()
        session.set_missing_host_key_policy(AutoAddPolicy())
        session.connect(
            hostname, username=username, password=password,
            timeout=self.connect_timeout)
        self.sessions[mobile] = (session, datetime.now(), dialect)
        msg = 'Connected to %s' % hostname
        self.send(sender, mobile, msg, dialect)

    def ssh_close(self, mobile, sender=None):
        logging.info('Closing session for %s', mobile)
        session, timestamp, dialect = self.sessions.pop(mobile)
        session.close()
        self.send(sender, mobile, 'Disconnected', dialect)

    def ssh_exec(self, mobile, content, sender=None):
        logging.debug('Executing %s for %s', content, mobile)
        session, timestamp, dialect = self.sessions[mobile]
        stdin, stdout, stderr = session.exec_command(content, timeout=self.exec_timeout)
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
        self.send(sender, mobile, msg, dialect)

    def send(self, sender, recipient, content, dialect=None):
        if dialect is None:
            dialect = normal
        self.sms.send(sender, recipient, translator.translate(content, dialect))

