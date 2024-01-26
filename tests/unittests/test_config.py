import os
import pytest
from pathlib import Path
from utils.config import load_env


# Updated fixture to avoid clearing pytest's internal variables
@pytest.fixture(autouse=True)
def clean_environment():
    # Save pytest's internal variable
    pytest_current_test = os.environ.get('PYTEST_CURRENT_TEST')

    # Clear environment variables selectively
    for key in list(os.environ.keys()):
        if key != 'PYTEST_CURRENT_TEST':
            del os.environ[key]

    yield

    # Restore pytest's internal variable after test
    if pytest_current_test:
        os.environ['PYTEST_CURRENT_TEST'] = pytest_current_test
    else:
        os.environ.pop('PYTEST_CURRENT_TEST', None)


# Use Pytest's powerful fixture system to manage env paths
@pytest.fixture
def env_path():
    return Path("config/.env")


@pytest.fixture
def non_existing_env_path():
    return Path("config_none/.env")


@pytest.fixture
def invalid_env_path():
    return Path("mockdata/fake.env")


def test_load_env_with_existing_env_file(env_path: Path):
    # Arrange
    expected_env_var = "test_value"
    os.environ["API_KEY"] = expected_env_var
    # Act
    result = load_env("API_KEY", env_path=env_path)
    # Assert
    assert result == expected_env_var


def test_load_env_with_non_existing_env_file(non_existing_env_path: Path):
    # Act
    result = load_env("API_KEY", env_path=non_existing_env_path)
    # Assert
    assert result is None


def test_load_env_with_invalid_env_file(invalid_env_path: Path):
    # Act
    result = load_env("API_KEY", env_path=invalid_env_path)
    # Assert
    assert result is None


def test_load_env_with_missing_env_var(invalid_env_path: Path):
    # Explicitly ensure API_KEY is not set
    os.environ.pop('API_KEY', None)

    # Assert that the environment variable is not defined before the test
    assert 'API_KEY' not in os.environ

    # Act
    result = load_env("API_KEY", env_path=invalid_env_path)

    # Assert
    assert result is None
