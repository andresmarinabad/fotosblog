import pytest
from unittest.mock import patch, MagicMock
import subprocess
import requests
import signal
from utils import start_celery_workers, start_redis_manual, signal_handler, download_images_from_target


# Simulación de config
class MockConfig:
    token = "fake_token"
    endpoints = {
        'target1': 'http://example.com/target1',  # Aseguramos que 'target1' esté definido
    }
    galeria = 'http://example.com/galeria/'


# Reemplazar config por nuestra clase MockConfig
@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    monkeypatch.setattr('config.config', MockConfig)


# Test para start_celery_workers
@patch('subprocess.Popen')
def test_start_celery_workers(mock_popen):
    # Simula que Popen se ejecuta correctamente
    mock_popen.return_value = MagicMock()

    start_celery_workers()

    # Verifica que el comando Popen fue llamado con los parámetros correctos
    mock_popen.assert_called_with([
        "celery",
        "-A", "celery_app",
        "worker",
        "--queues=images"
    ])


# Test para start_redis_manual
@patch('subprocess.Popen')
@patch('time.sleep', return_value=None)  # Evitar que time.sleep cause retrasos en las pruebas
def test_start_redis_manual(mock_sleep, mock_popen):
    # Simula que Popen se ejecuta correctamente y Redis se inicia
    mock_redis_process = MagicMock()
    mock_popen.return_value = mock_redis_process

    redis_process = start_redis_manual()

    # Verifica que el proceso de Redis se inicie correctamente
    mock_popen.assert_called_with(["redis-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert redis_process == mock_redis_process


# Test para signal_handler
@patch('subprocess.Popen')
@patch('sys.exit')
def test_signal_handler(mock_exit, mock_popen):
    # Simula que el comando de apagado de Celery y el killall se ejecutan correctamente
    mock_popen.return_value = MagicMock()

    # Simula la señal SIGINT
    signal_handler(signal.SIGINT, None)

    # Verifica que los comandos de cierre de Celery fueron ejecutados
    mock_popen.assert_any_call(["celery -A celery_app control shutdown"])
    mock_popen.assert_any_call(["killall celery"])
    mock_exit.assert_called_with(0)
