import os
from setuptools import setup

# Utility function to read the boilerplate files
def read_md(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pytest-ethereum",
    version='0.1.0a3',
    description='py.test plugin for testing Ethereum smart contracts',
    license='MIT',
    #long_description=read_md('README.md'),
    author='Bryant Eisenbach',
    author_email='bryant@dappdevs.org',
    url='https://github.com/fubuloubu/pytest-ethereum',
    python_requires='>=3.6',
    packages = ['pytest_ethereum'],
    install_requires=[
        'pytest>=3.4.1',
        'eth-tester[pyethereum21]',  # eventually switch to py-evm backend
        'web3>=4.0.0b11',
    ],

    # the following makes a plugin available to pytest
    entry_points = {
        'pytest11': [
            'name_of_plugin = pytest_ethereum.plugin',
        ]
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        # custom PyPI classifier for pytest plugins
        "Framework :: Pytest",
    ],
)
