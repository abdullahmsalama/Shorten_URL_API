"""
This file give some shared resources for the tests.
"""

import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app.api import app
from app.db import SessionLocal


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
