# Global Fixtures can be defined in this file
import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app=app)
    yield client  # testing happens here
