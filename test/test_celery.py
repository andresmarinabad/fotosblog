import pytest
from unittest.mock import MagicMock
from celery_app import download_image  # Cambia por la ubicación correcta del archivo que contiene la tarea
import requests
import os

@pytest.fixture
def mock_dependencies(mocker):
    mock_image_exists = mocker.patch('celery_app.image_exists', return_value=False)
    mock_insert_image = mocker.patch('celery_app.insert_image')
    mock_get = mocker.patch('requests.get', return_value=MagicMock(status_code=200, iter_content=lambda chunk_size: [b'fake_image_data']))
    mock_makedirs = mocker.patch('os.makedirs')
    mock_get_output = mocker.patch('celery_app.config.get_output', return_value='/mock/directory')

    return {
        'image_exists': mock_image_exists,
        'insert_image': mock_insert_image,
        'get': mock_get,
        'makedirs': mock_makedirs,
        'get_output': mock_get_output
    }

def test_download_image(mock_dependencies):
    mock_dependencies['image_exists'].return_value = False
    url = 'http://example.com/fake_image.jpg'
    target = 'target_directory'
    result = download_image(url, target)
    mock_dependencies['get'].assert_called_once_with(url, stream=True)
    mock_dependencies['makedirs'].assert_called_once_with('/mock/directory', exist_ok=True)
    assert result == False

def test_download_image_existing(mock_dependencies):
    mock_dependencies['image_exists'].return_value = True
    url = 'http://example.com/fake_image.jpg'
    target = 'target_directory'
    result = download_image(url, target)
    mock_dependencies['get'].assert_called_once()
    mock_dependencies['insert_image'].assert_not_called()
    assert result == False

def test_download_image_failure(mock_dependencies):
    mock_dependencies['get'].side_effect = requests.exceptions.RequestException("Network error")
    url = 'http://example.com/fake_image.jpg'
    target = 'target_directory'
    result = download_image(url, target)
    assert result == False
