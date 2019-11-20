#!/usr/bin/env python3

from apps import flask_app, custom_app, django_app
from server import WSGIServer

server = WSGIServer(host='localhost', port=8000)
if __name__ == '__main__':
    try:
        server.run(django_app)
    except KeyboardInterrupt:
        server.stop()
