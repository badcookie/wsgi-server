import pytest
import requests
from functools import partial
from multiprocessing import Process

from apps import django_app
from server import WSGIServer

from apps.bikes.bikes_site.models import Company, Category, Product

url = 'api/v1/'


@pytest.yield_fixture(scope='module', autouse=True)
def server():
    wsgi_server = WSGIServer('127.0.0.1', 8000)
    runner = partial(wsgi_server.run, django_app)
    server_process = Process(target=runner)
    server_process.start()
    yield server_process
    server_process.terminate()


@pytest.yield_fixture
def company():
    instance = Company.objects.create(name='yamamoto')
    yield instance
    instance.delete()


@pytest.yield_fixture
def category():
    instance = Category.objects.create(name='bikes')
    yield instance
    instance.delete()


@pytest.yield_fixture
def product():
    instance = Product.objects.create(
        name='rapunzel', category='bikes', company='yamamoto'
    )
    yield instance
    instance.delete()


def test_get(base_url, category):
    path = 'categories'
    full_url = f'{base_url}{url}{path}'
    response = requests.get(full_url)
    assert response.status_code == 200


