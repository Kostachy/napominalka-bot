import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    pass