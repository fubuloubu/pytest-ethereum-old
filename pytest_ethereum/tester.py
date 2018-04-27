import pytest

from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider

from eth_tester import EthereumTester
from eth_tester.exceptions import TransactionFailed

from .account import Account
from .contract import ContractFactory


class Tester:
    def __init__(self, compiled_interfaces):
        self.__t = EthereumTester()
        self.__w3 = Web3(EthereumTesterProvider(self.__t))

        # Empty by default, but can be set on initialization
        self.__compiled_interfaces = compiled_interfaces

        # TODO Set starting balance for all accounts to something very high
        #      and blk gas limit for chain to something approaching average

    def contracts(self, name):
        if ':' not in name:
            # If you don't specify which contract in file, use filebase
            name += ':{}'.format(name.split('/')[-1].split('.')[0])
        interface = self.__compiled_interfaces[name]
        return self.new_contract(interface)

    # alias
    def c(self, name):
        return self.contracts(name)

    def new_contract(self, interface):
        return ContractFactory(self.__w3, interface)
        
    @property
    def accounts(self):
        return [Account(self.__w3, a) for a in self.__t.get_accounts()]

    # Alias
    @property
    def a(self):
        return self.accounts
    
    @property
    def tx_fails(self):
        return FailureHandler(self.__t)

    def mine_blocks(self, number=1):
        self.__t.mine_blocks(number)

    def now(self):
        # TODO Get this from the Ethereum block timestamp
        return self.__w3.eth.getBlock('latest')['timestamp']

class FailureHandler:
    def __init__(self, eth_tester):
        self._t = eth_tester

    def __enter__(self):
        self._snapshot_id = self._t.take_snapshot()
        return self._snapshot_id
        
    def __exit__(self, *args):
        assert len(args) > 0 and \
            args[0] is TransactionFailed, \
                "Didn't revert transaction."
        self._t.revert_to_snapshot(self._snapshot_id)
        return True
