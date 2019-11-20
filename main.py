#!/usr/bin/env python3

from apps import flask_app, custom_app, django_app
from server import WSGIServer

server = WSGIServer(host='localhost', port=8000)
server.run(django_app)
