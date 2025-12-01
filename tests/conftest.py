
"""
Pytest configuration and shared fixtures for Phin Isan AI tests
"""

import pytest
import os
import shutil
from pathlib import Path


def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API keys"
    )


@pytest.fixture(scope="session")
def test_data_dir():
    """Create and provide test data directory"""
    data_dir = Path("test_data")
    data_dir.mkdir(exist_ok=True)
    yield data_dir
    # Cleanup after all tests
    # shutil.rmtree(data_dir)


@pytest.fixture
def clean_outputs():
    """Clean output directory before and after tests"""
    output_dir = Path("outputs")
    if output_dir.exists():
        for file in output_dir.glob("*"):
            if file.is_file():
                file.unlink()
    yield
    # Cleanup after test


@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock API keys for testing"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
    monkeypatch.setenv("QWEN_API_KEY", "test-qwen-key")


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Auto-mark tests that require API keys
    for item in items:
        if "OPENAI_API_KEY" in item.fixturenames:
            item.add_marker(pytest.mark.requires_api)
