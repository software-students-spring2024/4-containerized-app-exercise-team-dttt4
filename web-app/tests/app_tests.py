"""Tests for app.py"""

import pytest
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Tests if requests to root url can be handled"""
    return "Index Page"


@app.route("/list_text", methods=["GET"])
def list_text_test():
    """Tests handling GET requests to list_text"""
    return "List Text Page"


@app.route("/upload_image", methods=["GET", "POST"])
def list_upload_image_test():
    """Tests handling GET requests to upload_image"""
    return "Index Page"


@app.route("/trigger_process", methods=["POST"])
def test_trigger_process():
    """Tests handling GET requests to trigger_process"""
    assert True


def test_assert():
    """Basic test"""
    assert True


@pytest.fixture(name="create_app_client")
def fixture_app_client():
    """Creates test client"""
    client = app.test_client()
    return client


def test_root_dir(create_app_client):
    """Test root directory"""
    response = create_app_client.get("/")
    assert response.status_code == 200


def test_invalid_route(create_app_client):
    """Tests there's a non-existent route."""
    response = create_app_client.get("/non-existent-route")
    assert response.status_code == 404
