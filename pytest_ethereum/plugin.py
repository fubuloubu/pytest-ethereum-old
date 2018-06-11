import pytest

from .package import load_package
from .tester import Tester


# User can specify these options through execution flags
def pytest_addoption(parser):
    """Add options for contract assets file handling"""

    group = parser.getgroup('ethereum', 'ethereum testing support')
    group.addoption('--package-file', action='store', default=None, metavar='path',
            help='ERC190 Package Filename, default: none')


# Load assets file into memory
@pytest.fixture(scope='session')
def package(pytestconfig):
    package = {}
    package_file = pytestconfig.option.package_file
    if package_file:
        package = load_package(package_file)
    return package


# Fixture is initialized from default for every test
@pytest.fixture
def tester(package):
    return Tester(package)

# alias fixture
@pytest.fixture
def t(tester):
    return tester
