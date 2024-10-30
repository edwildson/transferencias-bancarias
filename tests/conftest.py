from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

import app


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)
