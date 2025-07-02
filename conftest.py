import pytest


@pytest.fixture(scope="module")
def shared_data():
    return {}
