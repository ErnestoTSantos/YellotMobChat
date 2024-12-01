import pytest
import sys

from django.db import connections
from django.db.backends.dummy import base

from rest_framework.test import APIClient

from tests.factory import UserFactory


@pytest.fixture(autouse=True)
def use_dummy_db():
    if "test" in sys.argv:
        connections["default"] = base.DatabaseWrapper(None, None)


@pytest.fixture
def user(client):
    user = UserFactory()
    return user


@pytest.fixture
def api_client():
    return APIClient()
