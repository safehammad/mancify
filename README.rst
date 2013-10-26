=======
Mancify
=======

SSH with a Manc flair! Coded at Hack Manchester, October 2013.

Don't have internet? Need to SSH into your server? Have your phone handy? Proud to be Mancunian? This app enables you to SSH into a server and communicate with it via SMS messaging. As an added bonus, you get to see your output in pure Mancunian dialect.

Setup
-----

* Sign up for an SMS package with Clockwork_ including an inbound mobile number. You'll be given an API Key.

* Place the API Key in `~/.mancify.ini` as follows::

    [mancify]
    clockwork_api_key=abcde12345

* Set up a server to serve the WSGI file in scripts/mancify.wsgi on port 80. Look `here <http://wsgi.readthedocs.org/>` for information on how to do this on your server. Make a note of the URL to which you have bound the WSGI file.

* Via the Clockwork_ website, point your inbound SMS number as a GET request to the URL to which you bound the WSGI file with '/sms' appended to it. For example, if you bound the WSGI file to http://www.myserver.com/mancify, then point the inbound SMS number to http://www.myserver.com/mancify/sms.

Give it a go!
-------------
Now you're all set to give it a go!

Connect to an SSH server by texting the following to your inbound number::

    ssh username@hostname password [dialect]

Where dialect is optional and can be "manc" (default) or "normal".

Now that you're connected, try out a command! Try texting some of the following (assuming your server recognises these commands):

* ls

* echo This is my house on the beach!

* fortune

Run the test server
-------------------
If you'd like to give this a go without having to set up a server on the internet, you can try this locally. You'll be able to receive text messages but you won't be able to send them (instead, you'll simulate sending a text message via your web browser).

Run the following::

    $ python test_server.py

Now simulate sending a text message by visiting the following URL in your web browser::

    http://localhost:8000/ssh?to=<clockwork_inbound_no>&from=<your_mobile_no>&content=<text_message>&msg_id=AB_1

Note that the message id can be any string but must be unique with each invocation.

So to connect to your server, use the following::

    http://localhost:8000/ssh?to=<clockwork_inbound_no>&from=<your_mobile_no>&content=hostname,username,password,dialect&msg_id=AB_1

And to run the "ls" command, use the following::

    http://localhost:8000/ssh?to=<clockwork_inbound_no>&from=<your_mobile_no>&content=ls&msg_id=AB_1

Try the translator
------------------
You might have noticed that by setting the dialect to "manc", you get pure Mancuian output! You can try out the translator on its own.

For example::

    >>> from mancify.translator import translate
    >>> translate('This is bad!')
    'This iz pants!'

Requirements
------------

See `requirements.txt` for details.

Testing
-------
To test in Python 2.7+::

    python -m unittest discover


.. _Clockwork: http://www.clockworksms.com/
