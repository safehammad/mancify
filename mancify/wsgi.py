from __future__ import (
    unicode_literals,
    absolute_import,
    division,
    print_function,
    )

# Make Py2's str type like Py3's
str = type('')

import logging
import socket
from datetime import datetime

from paramiko import SSHClient, AutoAddPolicy, SSHException
from wheezy.routing import PathRouter, url
from webob import Request, Response, exc
from clockwork import clockwork

import translator
import dialects.manc
import dialects.normal

DIALECTS = { 
    "manc":     dialects.manc,
    "normal":   dialects.normal,
}

# Maximum length of an SMS message (with triple concatenation, the maximum
# permitted under GSM)
SMS_MAX_LENGTH = 459


class MancifyWsgiApp(object):
    def __init__(self, **kwargs):
        super(MancifyWsgiApp, self).__init__()
        self.sms_api = clockwork.API(kwargs['clockwork_api_key'])
        self.exec_timeout = kwargs.get('exec_timeout', 10)
        self.connect_timeout = kwargs.get('connect_timeout', 30)
        self.session_timeout = kwargs.get('session_timeout', 300)
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
        if mobile in self.sessions:
            if content == '^D' or content == 'logout':
                self.ssh_close(mobile, sender)
            else:
                self.ssh_exec(mobile, content, sender)
        else:
            self.ssh_open(mobile, content, sender)
        raise exc.HTTPOk('Message processed')

    def ssh_open(self, mobile, content, sender=None):
        try:
            bits = content.split(',',3)             
            hostname, username, password = content[:3]
            dlname = bits[3] if len(bits)>3 else "manc"
        except ValueError:
            self.mobile_send(mobile,
                'Invalid connection request. Please send hostname,username,password[,dialect]')
        else:
            dialect = DIALECTS.get(dlname,dialects.manc)
            logging.info('Opening connection to %s for %s', hostname, username)
            try:
                session = SSHClient()
                session.set_missing_host_key_policy(AutoAddPolicy())
                session.connect(
                    hostname, username=username, password=password,
                    timeout=self.connect_timeout)
            except (socket.error, SSHException) as e:
                msg = str(e)
                if len(msg) > 140:
                    msg = msg[:137] + '...'
                self.mobile_send(mobile, msg, sender)
            else:
                self.sessions[mobile] = (session, datetime.now(),dialect)
                self.mobile_send(mobile, 'Connected to %s' % hostname, sender)

    def ssh_close(self, mobile, sender=None):
        logging.info('Closing session for %s', mobile)
        session, timestamp = self.sessions.pop(mobile)
        session.close()
        self.mobile_send(mobile, 'Ta very much!', sender)

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
        msg = translator.translate(msg,dialect)
        self.mobile_send(mobile, msg, sender)

    def mobile_send(self, mobile, content, sender=None):
        logging.debug('Sending message to %s', mobile)
        while content:
            # Send up to 459 characters at a time (the maximum length of a
            # triple concatenated SMS message)
            msg = clockwork.SMS(
                to=mobile, message=content[:SMS_MAX_LENGTH], from_name=sender)
            response = self.sms_api.send(msg)
            if not response.success:
                logging.error('%s %s', response.error_code, response.error_description)
            content = content[SMS_MAX_LENGTH:]

