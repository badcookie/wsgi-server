import json
import pytest
import requests
from functools import partial
from multiprocessing import Process

from apps import django_app
from server import WSGIServer

from bikes_site.models import Company, Category, Product

api_url = 'api/v1/'


@pytest.fixture(autouse=True)
def setup(transactional_db):
    Category.objects.create(name='bike')
    Category.objects.create(name='bus')

    Company.objects.create(name='yamamoto')

    Product.objects.create(
        company=Company.objects.get(name='yamamoto'),
        category=Category.objects.get(name='bike'),
        name='rapunzel',
    )

    wsgi_server = WSGIServer('127.0.0.1', 8000)
    runner = partial(wsgi_server.run, django_app)
    server_process = Process(target=runner)
    server_process.start()
    yield server_process
    server_process.terminate()


def test_get(base_url):
    url = f'{base_url}{api_url}'
    response = requests.get(f'{url}categories/')
    response_data = json.loads(response.content.decode('utf-8'))
    assert len(response_data) == 2
    assert response_data[1]['name'] == 'bus'
    assert response.status_code == 200

    response = requests.get(f'{url}categories/146')
    assert response.status_code == 404

    response = requests.get(f'{url}products/category/1/')
    response_data = json.loads(response.content.decode('utf-8'))
    result = response_data['results']
    assert response.status_code == 200
    assert result[0]['name'] == 'rapunzel'


def test_post(base_url):
    url = f'{base_url}{api_url}'
    full_url = f'{url}company/products/'
    data = {'company': 'yamamoto', 'category': 'bike', 'name': 'another_bike'}
    response = requests.post(full_url, data)
    assert response.status_code == 403
