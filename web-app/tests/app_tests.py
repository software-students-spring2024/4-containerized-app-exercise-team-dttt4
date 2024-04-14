import io
import os
import pytest
from flask import Flask
from pymongo import MongoClient
from PIL import Image
from bson import binary
from app import app, process_image, client, db, collection

def test_process_image_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'process_image.html' in response.data

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_image_post_no_file(mock_files, client):
    mock_files.get.return_value = None
    response = client.post('/')
    assert response.status_code == 200
    assert response.data == b'No file part'


def test_process_image_post_empty_file(mock_files, client):
    mock_file = mock_files.get.return_value
    mock_file.filename = ''
    response = client.post('/')
    assert response.status_code == 200
    assert response.data == b'No selected file'

def test_process_image_post_successful(mock_files, mock_image_open, client):
    mock_file = mock_files.get.return_value
    mock_file.filename = 'test.jpg'
    mock_image = mock_image_open.return_value
    mock_image_byte_array = io.BytesIO()
    mock_image.save.return_value = None
    mock_image.format = 'JPEG'
    response = client.post('/')
    assert response.status_code == 200
    assert response.data == b'Image successfully uploaded and added to MongoDB'

def test_process_image_post_mongodb_error(mock_files, mock_image_open, mock_insert_one, client):
    mock_file = mock_files.get.return_value
    mock_file.filename = 'test.jpg'
    mock_image = mock_image_open.return_value
    mock_image_byte_array = io.BytesIO()
    mock_image.save.return_value = None
    mock_image.format = 'JPEG'
    mock_insert_one.side_effect = Exception('MongoDB error')
    response = client.post('/')
    assert response.status_code == 500
    assert response.data == b'Error uploading image to MongoDB'
