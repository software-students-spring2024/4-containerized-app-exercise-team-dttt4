"""Tests for mlclient.py"""
from unittest.mock import patch, MagicMock 
import pytest
from flask import Flask
from mlclient import app, process, collection, db, fs
from PIL import Image

@pytest.fixture
def client():
    """Creates test client"""
    with app.test_client() as client:
        yield client

@patch('mlclient.collection')
def test_process_no_unprocessed_images (mock_collection, client): 
    mock_collection.find_one.return_value = None
    response = client.post('/process') 
    assert response.status_code == 404

@patch('mlclient.collection')
def test_process_io_error(mock_collection, client):
    mock_collection.find_one.side_effect= IOError("IO Error")
    response = client.post('/process') 
    assert response.status_code == 500

@patch('mlclient.collection')
@patch('mlclient.Image.open')
@patch('mlclient.pytesseract.image_to_string')
def test_process_successful(mock_pytesseract, mock_image_open, mock_collection, client):
    mock_collection.find_one.return_value = {'_id': '123', 'image_data': b'image_data', 'is_processed': False}
    mock_image_open.return_value = Image.new('RGB', (100, 100))
    mock_pytesseract.return_value = 'extracted text'
    response = client.post('/process')
    assert response.status_code == 200
    assert response.json == {'message': 'Image processed and text saved.'}
    mock_collection.update_one.assert_called_with(
        {'_id': '123'},
        {'$set': {'text': 'extracted text', 'is_processed': True}}
    )
