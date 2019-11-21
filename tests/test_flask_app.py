import pytest
import requests
from functools import partial
from multiprocessing import Process

from apps import flask_app
from server import WSGIServer


@pytest.yield_fixture(scope='module', autouse=True)
def server():
    wsgi_server = WSGIServer('127.0.0.1', 8000)
    runner = partial(wsgi_server.run, flask_app)
    server_process = Process(target=runner)
    server_process.start()
    yield server_process
    server_process.terminate()


def test_get(base_url):
    response = requests.get(base_url)
    assert response.text == 'Success'


def test_post(base_url):
    path = 'very_complex_query'
    data = {'yet_another_id': 9}
    response = requests.post(f'{base_url}{path}', data=data)
    assert response.status_code == 200
    assert response.text == '9'


