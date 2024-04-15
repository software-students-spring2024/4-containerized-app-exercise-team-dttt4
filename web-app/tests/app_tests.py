"""
This file contains tests for app.py
"""

import io

def test_process_image_get(test_client):
    """
    Tests if root url gives successful response 
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'process_image.html' in response.data

def client():
    """
    Sets up test up test client for flask 
    """
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_process_image_post_no_file(mock_files, client):
    """
    Tests if no file is uploaded
    """
    mock_files.get.return_value = None
    response = client.post('/')
    assert response.status_code == 200
    assert response.data == b'No file part'


def test_process_image_post_empty_file(mock_files, client):
    """
    Tests if empty file uploaded 
    """
    mock_file = mock_files.get.return_value
    mock_file.filename = ''
    response = client.post('/')
    assert response.status_code == 200
    assert response.data == b'No selected file'

def test_process_image_post_successful(mock_files, mock_image_open, client):
    """
    Tests if file successfully uploaded 
    """
    mock_file = mock_files.get.return_value
    mock_file.filename = 'test.jpg'
    mock_image = mock_image_open.return_value
    mock_image.save.return_value = None
    mock_image.format = 'JPEG'
    response = client.post('/')
    assert response.status_code == 200
    assert response.data == b'Image successfully uploaded and added to MongoDB'

def test_process_image_post_mongodb_error(mock_files, mock_image_open, mock_insert_one, client):
    """
    Tests if file has issues uploading 
    """
    mock_file = mock_files.get.return_value
    mock_file.filename = 'test.jpg'
    mock_image = mock_image_open.return_value
    mock_image.save.return_value = None
    mock_image.format = 'JPEG'
    mock_insert_one.side_effect = Exception('MongoDB error')
    response = client.post('/')
    assert response.status_code == 500
    assert response.data == b'Error uploading image to MongoDB'
