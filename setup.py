from setuptools import setup

setup(
    name="pytest-ethereum",
    version='0.1.0a21',
    description='py.test plugin for testing Ethereum smart contracts',
    long_description='TODO',
    license='MIT',
    author='Bryant Eisenbach',
    author_email='bryant@dappdevs.org',
    url='https://github.com/fubuloubu/pytest-ethereum',
    python_requires='>=3.6',
    packages = ['pytest_ethereum'],
    install_requires=[
        'pytest>=3.6.1,<4.0.0',
        'eth-tester[py-evm]==0.1.0-beta.32',
        'web3==4.7.1',
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
