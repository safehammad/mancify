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
import threading
from datetime import datetime

from paramiko import SSHClient, AutoAddPolicy, SSHException
from wheezy.routing import PathRouter, url
from webob import Request, Response, exc
from clockwork import clockwork

from mancify.sms import MancifySMSService
from mancify.ssh import MancifySSHSession

# Maximum length of an SMS message (with triple concatenation, the maximum
# permitted under GSM)
SMS_MAX_LENGTH = 459


class MancifyWsgiApp(object):
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
        self.lock = threading.Lock()
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
        msg_id = req.params['msg_id']
        recipient = req.params['from']
        sender = req.params['to']
        content = req.params['content']
        # If we've seen the message before it's a duplicate. Return 200 OK so
        # the server doesn't keep retrying but otherwise ignore it
        if msg_id in self.messages:
            raise exc.HTTPOk('Message already processed')
        self.messages.add(msg_id)
        try:
            with self.lock:
                try:
                    session = self.sessions[recipient]
                except KeyError:
                    session = MancifySSHSession(
                        self.sms, sender, recipient,
                        self.connect_timeout, self.exec_timeout)
                    self.sessions[recipient] = session
                else:
                    session.timestamp = datetime.now()
            session.execute(content)
        except Exception as e:
            msg = str(e)
            if len(msg) > 140:
                msg = msg[:137] + '...'
            self.sms.send(sender, recipient, msg)
        raise exc.HTTPOk('Message processed')

