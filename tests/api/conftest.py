import pytest
from pytest_ethereum.tester import Tester

@pytest.fixture
def t():
    return Tester()
