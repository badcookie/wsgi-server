import json

import pytest
from django.test import Client

from .models import Category, Company, Motobike


@pytest.fixture
def setup(transactional_db):
    Category.objects.create(name='Мотоциклы')
    Category.objects.create(name='Мопеды')
    Category.objects.create(name='Квадроциклы')

    Company.objects.create(name='Kawasaki')
    Company.objects.create(name='Honda')

    Motobike.objects.create(
        company=Company.objects.get(name='Honda'),
        category=Category.objects.get(name='Мопеды'),
        name='Giorno',
    )

    Motobike.objects.create(
        company=Company.objects.get(name='Kawasaki'),
        category=Category.objects.get(name='Мотоциклы'),
        name='Ninja',
    )

    Motobike.objects.create(
        company=Company.objects.get(name='Kawasaki'),
        category=Category.objects.get(name='Мотоциклы'),
        name='Ninja Turbo',
    )


def test_models(setup):
    assert Company.objects.get(motobike__name='Giorno').name == 'Honda'
    assert Category.objects.get(motobike__name='Ninja').name == 'Мотоциклы'


def test_index():
    client = Client()
    response = client.get('')
    assert response.status_code == 200
    assert response.content == b"Hello, world. You're at the index."


def test_categories(setup):
    client = Client()
    response = client.get('/categories/')
    assert response.status_code == 200
    assert json.loads(response.content.decode('utf-8'))[2]['name'] == 'Квадроциклы'


def test_category(setup):
    client = Client()
    category_id = Category.objects.get(name='Мотоциклы').id
    response = client.get(f'/categories/{category_id}/')
    assert response.status_code == 200
    response_data = json.loads(response.content.decode('utf-8'))
    assert len(response_data) == 2
    assert response_data[1]['name'] == 'Ninja Turbo'
    assert response_data[1]['vendor'] == 'Kawasaki'
    assert response_data[1]['category'] == 'Мотоциклы'
    assert response_data[1]['description'] == ''

    response = client.get(f'/categories/25/')
    assert response.status_code == 404


def test_details(setup):
    client = Client()
    motobike_id = Motobike.objects.get(name='Ninja').id
    response = client.get(f'/details/{motobike_id}/')

    assert response.status_code == 200

    response_data = json.loads(response.content.decode('utf-8'))
    assert response_data['name'] == 'Ninja'
    assert response_data['vendor'] == 'Kawasaki'
    assert response_data['category'] == 'Мотоциклы'
    assert response_data['description'] == ''

    response = client.get(f'/details/25/')
    assert response.status_code == 404
