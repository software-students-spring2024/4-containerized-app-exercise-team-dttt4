import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
import pytest
from flask import template_rendered
from contextlib import contextmanager
import io
import requests


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mocker():
    from mongomock import MongoClient
    mocker = MongoClient()
    app.db = mocker["imagedb"]
    app.collection = app.db["imageCollection"]
    return app.collection


@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def test_home_page(client):
    """Test the home page loads properly."""
    response = client.get('/')
    assert response.status_code == 200


def test_image_upload(client, mocker):
    """Test uploading an image successfully."""
    with captured_templates(app) as templates:
        data = {'file': (io.BytesIO(b"fake image data"), 'test.jpg')}
        response = client.post('/', data=data, content_type='multipart/form-data')
        assert response.status_code == 200


def test_list_text(client, mocker):
    """Test the listing of processed images."""
    mocker.insert_one({"image_name": "test.jpg", "is_processed": True, "text": "Sample text"})
    response = client.get('/list_text')
    assert response.status_code == 200


def test_trigger_process(client, mocker):
    """Test the processing trigger."""
    response = client.post('/trigger_process')
    assert response.status_code == 302
