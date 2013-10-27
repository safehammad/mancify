=======
Mancify
=======

SSH with a Manc flair! Coded at Hack Manchester, October 2013.

Don't have internet? Need to SSH into your server? Have your phone handy? Proud
to be Mancunian? This app enables you to SSH into a server and communicate with
it via SMS messaging. As an added bonus, you get to see your output in pure
Mancunian dialect.


Setup
-----

* Install the package with ``python setup.py install``.

* Sign up for an SMS package with `Clockwork`_ including an inbound SMS number.
  You'll be given an API Key.

* Via the `Clockwork`_ website, configure your inbound SMS number to perform a
  GET request to the URL to which you will bind the application with "/ssh"
  appended to it. For example, if you bind the application to
  http://www.myserver.com/mancify, then point the inbound SMS number to
  http://www.myserver.com/mancify/ssh. Note that the Clockwork API requires
  your web-server to be running on port 80 (or port 443 with a valid cert).

* Place your `Clockwork`_ API Key in ``~/.mancify.ini`` like so::

    [mancify]
    clockwork_api_key=abcde12345

Now you are ready to run the server. The simple way of doing this is to run
``sudo mancify`` which will run the server on port 80 (remember that Clockwork
requires this). However, this obviously assumes you don't already have a
web-server (like Apache) running on port 80.

If you wish to integrate the application with an existing web-server, visit
http://wsgi.readthedocs.org/ for information on integrating WSGI applications
with your web-server (e.g. using mod_wsgi with Apache). The WSGI application
script that you want to serve is found under ``scripts/mancify.wsgi``.


Give it a go!
-------------

Connect to an SSH server by texting the following to your inbound SMS number::

    ssh username@hostname password [dialect]

Where dialect is optional and can be "manc", the Mancunian dialect (default),
or "normal".

Now that you're connected, try out a command! Try texting some of the following
(assuming your server recognises these commands):

* ``ls``

* ``echo This is my house on the beach!``

* ``fortune``


Testing the server
------------------

If you'd like to try this without having to set up a server on the internet,
you can run a server locally. You'll be able to receive text messages but you
won't be able to send them (instead you can simulate sending a text message via
your web browser).

Simply run ``mancify`` which will bind the server to localhost:8000. Now
simulate sending a text message by visiting the following URL in your web
browser::

    http://localhost:8000/ssh?to=<inbound_sms_no>&from=<your_mobile_no>&content=<text_message>&msg_id=AB_1

Note that "msg_id" represents the message id which can be any string but must
be unique with each invocation.

To open an SSH connection to your server, use the following::

    http://localhost:8000/ssh?to=<inbound_sms_no>&from=<your_mobile_no>&content=ssh+username@hostname+password+dialect&msg_id=AB_1

And run the "ls" command with the following URL::

    http://localhost:8000/ssh?to=<inbound_sms_no>&from=<your_mobile_no>&content=ls&msg_id=AB_2


Try the translator
------------------

You might have noticed that by setting the dialect to "manc" you get pure
Mancuian output! You can try out the translator on its own.

For example::

    >>> from mancify.translator import translate
    >>> translate('This is bad!')
    'This iz pants!'


Testing
-------

To test in Python 2.7+::

    python -m unittest discover


.. _Clockwork: http://www.clockworksms.com/
