import json
import pytest
import requests

from apps import django_app, flask_app, custom_app
from bikes_site.models import Company, Category, Product


@pytest.fixture
def django_setup(transactional_db, start_server):
    Category.objects.create(name='bike')
    Category.objects.create(name='bus')

    Company.objects.create(name='yamamoto')

    Product.objects.create(
        company=Company.objects.get(name='yamamoto'),
        category=Category.objects.get(name='bike'),
        name='rapunzel',
    )

    return start_server(django_app)


def test_custom_app(base_url, start_server):
    for _ in start_server(custom_app):
        random_path = 'this_is_path'
        response = requests.get(f'{base_url}{random_path}')
        assert response.text == f'Hello from /{random_path}'

        response = requests.delete(f'{base_url}{random_path}')
        assert response.request.method == 'DELETE'


def test_flask_app(base_url, start_server):
    for _ in start_server(flask_app):
        response = requests.get(base_url)
        assert response.text == 'Success'

        path = 'very_complex_query'
        data = {'yet_another_id': 9}
        response = requests.post(f'{base_url}{path}', data=data)
        assert response.status_code == 200
        assert response.text == '9'


def test_django_app(base_url, django_setup):
    for _ in django_setup:
        api_url = 'api/v1/'

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

        url = f'{base_url}{api_url}'
        full_url = f'{url}company/products/'
        data = {'company': 'yamamoto', 'category': 'bike', 'name': 'another_bike'}
        response = requests.post(full_url, data)
        assert response.status_code == 403


