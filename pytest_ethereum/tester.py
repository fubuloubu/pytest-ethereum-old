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
        
        # TODO Set starting balance for all accounts and gas limit for chain
        # NOTE Chain auto-mines transactions vs before

    def contracts(self, name):
        if ':' not in name:
            # If you don't specify which contract in file, use filebase
            name += ':{}'.format(name.split('/')[-1].split('.')[0])
        interface = self.__compiled_interfaces[name]
        return self.new_contract(interface)

    def new_contract(self, interface):
        return ContractFactory(self.__w3, interface)
        
    @property
    def accounts(self):
        return [Account(self.__w3, a) for a in self.__t.get_accounts()]
    
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
