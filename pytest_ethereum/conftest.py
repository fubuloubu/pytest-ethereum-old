import pytest

from web3 import Web3
from web3.contract import ImplicitContract
from web3.providers.eth_tester import EthereumTesterProvider

from eth_tester import EthereumTester
from eth_tester.exceptions import TransactionFailed

from .account import Account
from .contract import ContractFactory
from .asset_loader import get_assets


class Tester:
    def __init__(self):
        self._t = EthereumTester()
        self._w3 = Web3(EthereumTesterProvider(self._t))
        self._compiled_interfaces = get_assets()  # This needs to somehow be configurable
        
        # TODO Set starting balance for all accounts and gas limit for chain
        # NOTE Chain auto-mines transactions vs before

    def contracts(self, name):
        if ':' not in name:
            # If you don't specify which contract in file, use filebase
            name += ':{}'.format(name.split('/')[-1].split('.')[0])
        interface = self._compiled_interfaces[name]
        return self.new_contract(interface)

    def new_contract(self, interface):
        return Contract(self._w3, interface)
        
    @property
    def accounts(self):
        return [Account(self._w3, a) for a in self._t.get_accounts()]
    
    @property
    def tx_fails(self):
        return pytest.raises(TransactionFailed)

    # TODO Potentially replace with TestContract.pastEvents
    def get_log(contract, event_name):
        #TODO Filter by contract and event_name
        #     contract either by address or ABI
        filter_id = t.create_log_filter()
        #TODO Should return decoded event log receipt
        return t.get_only_fiter_changes(filter_id)


@pytest.fixture
def tester():
    return Tester()
