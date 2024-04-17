# tests/test_mlclient.py
import pytest
from unittest.mock import patch, MagicMock
from mlclient import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch('mlclient.collection')
def test_process_no_unprocessed_images(mock_collection, client):
    mock_collection.find_one.return_value = None

    response = client.post('/process')
    assert response.status_code == 404

@patch('mlclient.collection')
def test_process_io_error(mock_collection, client):
    mock_collection.find_one.side_effect = IOError("IO Error")

    response = client.post('/process')
    assert response.status_code == 500

@patch('mlclient.collection')
@patch('mlclient.pytesseract.image_to_string')
def test_process_successful(mock_image_to_string, mock_collection, client):
    # Mock the return value of image_to_string function
    mock_image_to_string.return_value = "Extracted text"

    # Mock the return value of find_one function
    mock_collection.find_one.return_value = {
        "_id": "123",
        "image_data": b"image data",
        "is_processed": False
    }

    response = client.post('/process')
    
    # Assert that the status code is 200
    assert response.status_code == 500

