import pytest
from functools import partial
from multiprocessing import Process

from server import WSGIServer


DEFAULT_PORT = 8000


@pytest.fixture
def base_url():
    return f'http://localhost:{DEFAULT_PORT}/'


@pytest.fixture
def start_server():
    def server(app):
        wsgi_server = WSGIServer('127.0.0.1', DEFAULT_PORT)
        runner = partial(wsgi_server.run, app)
        server_process = Process(target=runner)
        server_process.start()
        yield server_process
        server_process.terminate()

    return server
