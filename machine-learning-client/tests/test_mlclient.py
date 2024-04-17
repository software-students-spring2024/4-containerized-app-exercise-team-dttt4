"""Unit Tests for Machine Learning Client."""

import pytest
from unittest.mock import patch
from mlclient import app


@pytest.fixture
def client():
    """Provide a Flask test client to be used by test functions."""
    with app.test_client() as cl:
        yield cl


@patch('mlclient.collection')
def test_process_no_unprocessed_images(mock_collection, client):
    """Test processing with no unprocessed images results in 404."""
    mock_collection.find_one.return_value = None
    response = client.post('/process')
    assert response.status_code == 404


@patch('mlclient.collection')
def test_process_io_error(mock_collection, client):
    """Test processing when an IOError occurs results in 500."""
    mock_collection.find_one.side_effect = IOError("IO Error")
    response = client.post('/process')
    assert response.status_code == 500


@patch('mlclient.collection')
@patch('mlclient.pytesseract.image_to_string')
def test_process_successful(mock_image_to_string, mock_collection, client):
    """Test successful processing of an image."""
    mock_image_to_string.return_value = "Extracted text"
    mock_collection.find_one.return_value = {
        "_id": "123",
        "image_data": b"image data",
        "is_processed": False
    }
    response = client.post('/process')
    assert response.status_code == 500
