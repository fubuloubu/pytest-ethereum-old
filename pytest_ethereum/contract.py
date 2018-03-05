from web3 import Web3
from web3.contract import ImplicitContract

from .utils import clean_modifiers


class ContractInstance:
    """Deployed instance of a contract"""

    def __init__(self, w3: Web3, address, interface):
        self.__w3 = w3
        self.__address = address
        self.__instance = self.__w3.eth.contract(self.__address, **interface,
                ContractFactoryClass=ImplicitContract)
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.__w3.eth.filter({'address': self.__address})

    def __getattr__(self, name):
        """Delegates to either specialized methods or instance ABI"""
        if name in dir(self):
            # Specialized testing methods
            return getattr(self, name)
        else:
            # Method call of contract instance
            #TODO: This doesn't work!
            return getattr(self.__instance, name)

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

    @property
    def new_logs(self):
        """Returns all the event logs added since last checked for this contract"""
        return self.__filter.get_new_entries()

    @property
    def all_logs(self):
        return self.__filter.get_all_entries()


class ContractFactory:
    """Factory (prototype) of a contract"""
    def __init__(self, w3: Web3, interface):
        self.__w3 = w3
        self.__interface = interface
        self.__contract_factory = self.__w3.eth.contract(**self.__interface)

    def deploy(self, *args, **kwargs):
        """Deploy a new instance of this contract"""

        #TODO: HACK, awaiting resolution of web3.py/#666
        if 'transact' in kwargs.keys():
            kwargs['transaction'] = kwargs['transact']
            del kwargs['transact']

        # Our encapsulating classes need to be evaluated here
        # in order to avoid bugs when web3 processes our modifiers
        kwargs = clean_modifiers(kwargs)

        tx_hash = self.__contract_factory.deploy(args=args, **kwargs)
        address = self.__w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return ContractInstance(self.__w3, address, self.__interface)
