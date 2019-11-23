import click
import logging
from typing import Any

from server import WSGIServer
from apps import flask_app, custom_app, django_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')


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
        logger.info('Launching server at port %d', port)
        application = apps[app]
        server.run(application)
    except KeyboardInterrupt:
        logger.info('Stopping server.')
        server.stop()


if __name__ == '__main__':
    main()

