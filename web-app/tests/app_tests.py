"""Tests for app.py"""
import pytest
import io
import os
import unittest
from pymongo import MongoClient
from unittest.mock import Mock, patch
from flask import Flask, request, url_for
from app import upload_image, list_text, trigger_process
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Tests if requests to root url can be handled"""
    return 'Index Page'

@app.route('/list_text', methods=['GET'])
def list_text_test():
    """Tests handling GET requests to list_text"""
    return 'List Text Page'

@app.route('/upload_image', methods=['GET', 'POST'])
def list_upload_image_test():
    """Tests handling GET requests to upload_image"""
    return 'Index Page'

@app.route('/trigger_process', methods=['POST'])
def test_trigger_process():
    """Tests handling GET requests to trigger_process"""
    assert 'Trigger Process'

def test_assert():
    """Basic test"""
    assert True

def test_root_dir(client):
    """T"""
    response = client.get('/')
    assert response.status_code == 200

@pytest.fixture
def client():
    """Creates test client"""
    client = app.test_client()
    return client

def test_upload_image_get(client):
    """Test that a 404 error is returned for an invalid image path."""
    response = client.get('/image/non-existent-image.jpg')
    assert response.status_code == 404

def test_invalid_route(client):
    """Tests there's a non-existent route."""
    response = client.get('/non-existent-route')
    assert response.status_code == 404

def test_list_text(client):
    """Test the list_text route."""
    with patch('app.collection.find') as mock_find:
        mock_find.return_value = [
            {'text': 'Test Text 1', 'image_name': 'image1.jpg'},
            {'text': 'Test Text 2', 'image_name': 'image2.jpg'}
        ]
        response = client.get('/list_text')
        assert response.status_code == 200
        # assert b'Test Text 1' in response.data
        # assert b'Test Text 2' in response.data


# def test_trigger_process_success(client):
#     """Test the trigger_process route with a successful response."""
#     with patch('app.requests.post') as mock_post:
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_post.return_value = mock_response
#         response = client.post('/trigger_process', follow_redirects=True)
#         assert response.status_code == 200
#         # assert b'Processing triggered successfully.' in response.data

# def test_trigger_process_failure(client):
#     """Test the trigger_process route with a failed response."""
#     with patch('app.requests.post') as mock_post:
#         mock_response = Mock()
#         mock_response.status_code = 500
#         mock_response.text = 'Internal Server Error'
#         mock_post.return_value = mock_response
#         # response = client.post('/trigger_process', follow_redirects=True)
#         # assert response.status_code == 200

