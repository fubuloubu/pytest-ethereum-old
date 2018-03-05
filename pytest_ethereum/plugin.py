import pytest

from .assets import get_assets
from .tester import Tester


# User can specify these options through execution flags
def pytest_addoption(parser):
    """Add options for contract assets file handling"""

    group = parser.getgroup('ethereum', 'ethereum testing support')
    group.addoption('--assets-file', action='store', default=None, metavar='path',
            help='assets file for coverage, default: none')


# Load assets file into memory
@pytest.fixture(scope='session')
def assets(pytestconfig):
    assets = {}
    assets_file = pytestconfig.option.assets_file
    if assets_file:
        assets = get_assets(assets_file)
    return assets


# Fixture is initialized from default for every test
@pytest.fixture
def tester(assets):
    return Tester(assets)
