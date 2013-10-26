import sys
import logging
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.INFO)
from wsgiref.simple_server import make_server

# Import wsgi application
execfile('scripts/mancify.wsgi')

httpd = make_server('', 8000, application)
httpd.serve_forever()
