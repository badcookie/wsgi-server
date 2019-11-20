#!/usr/bin/env python3

import click
from typing import Any

from server import WSGIServer
from apps import flask_app, custom_app, django_app


apps = {
    'django': django_app,
    'flask': flask_app,
    'custom': custom_app
}


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=8000)
@click.option('--app', required=True, type=click.Choice(apps.keys()))
def main(host: str, port: int, app: Any) -> None:
    server = WSGIServer(host=host, port=port)
    try:
        application = apps[app]
        server.run(application)
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()

