import pytest
import json
import os
from unittest import mock
from config import Config

# Datos simulados para el archivo JSON
mock_config_data = {
    "endpoints": {"test": "http://example.com"},
    "token": "12345",
    "galeria": "test_gallery"
}


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data=json.dumps(mock_config_data))
@mock.patch("json.load", return_value=mock_config_data)
def test_config_init(mock_json_load, mock_open):
    """Prueba la inicialización de Config y la lectura del archivo JSON."""
    config = Config()
    assert config.endpoints == mock_config_data["endpoints"]
    assert config.token == mock_config_data["token"]
    assert config.galeria == mock_config_data["galeria"]
    assert config.output == os.path.expanduser("~/Pictures")
    assert config.default == os.path.expanduser("~/Pictures")
    mock_open.assert_called_once_with("data/conf.json", "r")
    mock_json_load.assert_called_once()


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data=json.dumps(mock_config_data))
@mock.patch("json.dump")
def test_config_save(mock_json_dump, mock_open):
    """Prueba la función save() para escribir el archivo JSON."""
    with mock.patch("json.load", return_value=mock_config_data):
        config = Config()

    config.endpoints = {"new": "http://new-example.com"}
    config.token = "67890"
    config.galeria = "new_gallery"
    config.save()

    expected_data = {
        "endpoints": config.endpoints,
        "token": config.token,
        "galeria": config.galeria
    }

    mock_open.assert_any_call("data/conf.json", "r")
    mock_open.assert_any_call("data/conf.json", "w")
    mock_json_dump.assert_called_once_with(expected_data, mock.ANY, indent=4)


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data=json.dumps(mock_config_data))
def test_get_output(mock_open):
    """Prueba la función get_output()."""
    config = Config()
    target = "test_folder"
    expected_path = os.path.join(config.output, target)
    assert config.get_output(target) == expected_path
