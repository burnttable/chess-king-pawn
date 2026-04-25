import pytest
import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """Create a test Flask app"""
    from app import create_app
    app = create_app('testing')
    return app
