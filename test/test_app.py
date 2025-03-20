import pytest
import sys
from app import main
from config import config


@pytest.fixture
def mock_dependencies(mocker):
    mock_isdir = mocker.patch('os.path.isdir', return_value=True)
    mock_download = mocker.patch('utils.download_images_from_target')
    mock_endpoints = mocker.patch.object(config, 'endpoints', {'target1': 'http://example.com'})
    mock_save = mocker.patch.object(config, 'save')

    return {
        'isdir': mock_isdir,
        'download_images_from_target': mock_download,
        'endpoints': mock_endpoints,
        'save': mock_save
    }


def test_list_targets(mock_dependencies, capsys):
    sys.argv = ['app.py', '--list']
    main()
    captured = capsys.readouterr()
    assert 'Available targets:' in captured.out
    assert 'target1' in captured.out


def test_invalid_target(mock_dependencies, capsys):
    sys.argv = ['app.py', '--target', 'invalid_target', '--output', '/mock/directory']
    main()
    captured = capsys.readouterr()
    assert 'Error: target not valid' in captured.out


def test_configure_target(mock_dependencies, capsys):
    sys.argv = ['app.py', '--configure', 'new_endpoint', '--target', 'target1']
    main()
    mock_dependencies['save'].assert_called_once()
    assert config.endpoints['target1'] == 'new_endpoint'


def test_missing_target_for_output(mock_dependencies, capsys):
    sys.argv = ['app.py', '--output', '/mock/directory']
    main()
    captured = capsys.readouterr()
    assert 'Error: you need to specify a target' in captured.out

