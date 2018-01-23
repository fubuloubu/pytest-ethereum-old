from setuptools import setup

setup(
    name="pytest-ethereum",
    version='0.1.0',
    description='py.test plugin for testing Ethereum smart contracts',
    author='Bryant Eisenbach',
    packages = ['pytest_ethereum'],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'name_of_plugin = pytest_ethereum.pluginmodule',
        ]
    },

    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
)
