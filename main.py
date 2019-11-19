#!/usr/bin/env python3

from apps import flask_app, app
from server import WSGIServer

server = WSGIServer(port=8000)
server.run(flask_app)
