"""
Contract Testing Fixtures and Utilities

----

Provided under MIT License:
Copyright 2017 Bryant Eisenbach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pytest
import json

from web3 import Web3
from web3.contract import ImplicitContract, ConciseContract
from web3.providers.eth_tester import EthereumTesterProvider
from eth_tester import EthereumTester
from eth_tester.exceptions import TransactionFailed


class TestContract(ImplicitContract):
    # Custom test-only methods and modifiers
    # Modifiers: 'fails()' replacing assert_tx_failed
    pass


@pytest.fixture
def t():
    t = EthereumTester()
    # Add convienence accounts e.g. t.a0/t.k0, t.a1/t.k1, ..., t.a9/t.k9
    accounts = t.get_accounts()
    [setattr(t, "a{}".format(i), a) for i, a in enumerate(accounts)]
    # Convienence Methods
    setattr(t, 'hascode', lambda a: t.get_code(a) != '0x')
    # TODO Set starting balance for all accounts and gas limit for chain
    # NOTE Chain auto-mines transactions vs before
    return t

@pytest.fixture
def web3(t):
    return Web3(EthereumTesterProvider(t))


from os.path import isfile as file_exists

# Move this to dynamically loaded or None
@pytest.fixture
def compiled_json():
    # TODO Make this configurable
    filename='../contracts/contracts.json'
    if file_exists(filename):
        with open(filename, 'r') as f:
            compiled_interfaces = json.loads(f.read())['contracts']
        # check proper structure e.g.
        # 'Contract1' : { 'abi' : ..., 'bytecode' : ..., 'bytecode_runtime' : ... }, 'Contract2' : ...
        required_members = ['abi', 'bytecode', 'bytecode_runtime']
        for name, interface in compiled_interfaces.items():
            filtered_interface = dict()
            for member in interface.keys():
                # Conversions for unique outputs
                if member == 'abi':
                    filtered_interface['abi'] = interface[member]
                if member == 'bin':
                    filtered_interface['bytecode'] = interface[member]
                if member == 'bin-runtime':
                    filtered_interface['bytecode_runtime'] = interface[member]
            for member in required_members:
                assert member in filtered_interface.keys(), "Contract '{}' doesn't have '{}'!".format(name, member)
            compiled_interfaces[name] = filtered_interface
    else:
        compiled_interfaces = None
    return compiled_interfaces

@pytest.fixture
def get_balance(t):
    # TODO Just replace all usages of this fixture with t.get_balance
    return t.get_balance

@pytest.fixture
def is_destroyed(t):
    # TODO This should be an added convienence method in eth-tester
    return lambda a: int(t.get_code(a)) == 0

@pytest.fixture
def contract_tester(web3, compiled_json):
    # NOTE use transact keyword because of compatibility with Web3.py transact modifier
    def contract_tester(contract=None, interface=None, args=None, transact=None):
        if not interface:
            # If contract_interface is not provided
            assert contract is not None, "Name must be provided if interface is not!"
            assert compiled_json is not None, "No compiled contracts found!"
            # If no contract in file is selected, assume file basename
            if ':' not in contract:
                contract += ':' + contract.split('/')[-1].split('.')[0]
            interface = compiled_json[contract]
        # NOTE: This process is convoluted due to implementation in Web3.py
        contract = web3.eth.contract(**interface)
        tx_hash = contract.deploy(transaction=transact, args=args)
        address = web3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        instance = web3.eth.contract(address, **interface, ContractFactoryClass=ImplicitContract)
        return instance
    return contract_tester

@pytest.fixture
def tx_fails():
    return pytest.raises(TransactionFailed)

# TODO Delete this
@pytest.fixture
def Token(contract_tester):
    return contract_tester(contract='ico/Token.sol:TokenNoDecimals', args=[b'', b'', 1000])

# TODO Potentially replace with TestContract.pastEvents
@pytest.fixture
def get_log(t):
    def get_log(contract, event_name):
        #TODO Filter by contract and event_name
        #     contract either by address or ABI
        filter_id = t.create_log_filter()
        #TODO Should return decoded event log receipt
        return t.get_only_fiter_changes(filter_id)
    return get_log
