from web3 import Web3
from web3.contract import ImplicitContract

from .log import Log
from .utils import (
        clean_modifiers,
        get_event_processors,
        get_event_signatures,
    )


class ContractInstance:
    """Deployed instance of a contract"""

    def __init__(self, w3: Web3, address, interface):
        self.__w3 = w3
        self.__address = address
        self.__instance = ImplicitContract(self.__w3.eth.contract(self.__address, **interface))
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.__w3.eth.filter({
                # Include events from the deployment stage
                'fromBlock': self.__w3.eth.blockNumber - 1,
                'address': self.__address
            })
        
        self.__event_signatures = get_event_signatures(interface['abi'])
        self.__event_processors = get_event_processors(interface['abi'])

    def __getattr__(self, name):
        """Delegates to either specialized methods or instance ABI"""
        if name in dir(self):
            # Specialized testing methods
            return getattr(self, name)
        elif name in self._events:
            return self._gen_log(name)
        else:
            # Method call of contract instance
            return getattr(self.__instance, name)

    @property
    def _events(self):
        return self.__event_signatures.keys()

    def _gen_log(self, name):
        return lambda v: Log(name, v)

    @property
    def address(self):
        """This contract's address"""
        return self.__address

    @property
    def balance(self):
        """Ether balance of this contract (in wei)"""
        return self.__w3.eth.getBalance(self.__address)

    @property
    def codesize(self):
        """Codesize of this contract (in bytes)"""
        return len(self.__w3.eth.getCode(self.__address)[2:])/2

    @property
    def hascode(self):
        """Check if this contract currently has code (usually indicating suicide)"""
        return self.codesize != 0

    def _process_logs(self, logs):
        processed_logs = []
        for log in logs:
            log_signature = log['topics'][0]
            if log_signature in self.__event_processors.keys():
                p_log = self.__event_processors[log_signature](log)
                processed_logs.append(Log(p_log['event'], p_log['args']))
        return processed_logs

    @property
    def logs(self):
        """Returns all the event logs ever added for this contract"""
        return self._process_logs(self.__filter.get_all_entries())


class ContractFactory:
    """Factory (prototype) of a contract"""
    def __init__(self, w3: Web3, interface):
        self.__w3 = w3
        self.__interface = interface
        self.__contract_factory = self.__w3.eth.contract(**self.__interface)

    def __call__(self, *args, **kwargs):
        """Deploy a new instance of this contract"""

        # Our encapsulating classes need to be evaluated here
        # in order to avoid bugs when web3 processes our modifiers
        kwargs = clean_modifiers(kwargs)

        # NOTE This is hacky, filing bug
        if 'transact' in kwargs.keys():
            kwargs['transaction'] = kwargs['transact']
            del kwargs['transact']

        tx_hash = self.__contract_factory.constructor(*args).transact(**kwargs)
        address = self.__w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return ContractInstance(self.__w3, address, self.__interface)

    def __getattr__(self, name):
        return getattr(self.__contract_factory, name)
