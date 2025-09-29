import pytest
from fastapi.testclient import TestClient

from todo_list_fastapi.app import app


@pytest.fixture
def client():
    return TestClient(app)
