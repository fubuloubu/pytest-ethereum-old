from web3 import Web3
from web3.contract import ImplicitContract


class ContractInstance:
    """Deployed instance of a contract"""

    def __init__(self, w3: Web3, address, interface):
        self.__w3 = w3
        self.__address = address
        self.__instance = self.__w3.eth.contract(self.__address, **interface,
                ContractFactoryClass=ImplicitContract)
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.__w3.eth.filter({'address': self.__address})
        #TODO: Figure out Web3.py logs API
        #self.__logs = self.__w3.utils.filters.LogFilter(self.__filter)

    def __getattr__(self, name):
        """Delegates to either specialized methods or instance ABI"""
        if name in dir(self):
            # Specialized testing methods
            return getattr(self, name)
        else:
            # Method call of contract instance
            return getattr(self.__instance, name)

    @property
    def address(self):
        """This contract's address"""
        return self.__address

    @property
    def balance(self):
        """Ether balance of this contract (in wei)"""
        return self.__w3.eth.getBalance(self.address)

    @property
    def codesize(self):
        """Codesize of this contract (in bytes)"""
        return len(self.__w3.eth.getCode(self.address)[2:])/2

    @property
    def hascode(self):
        """Check if this contract currently has code (usually indicating suicide)"""
        return self.codesize != 0

    @property
    def logs(self):
        """Returns all the event logs created (since last polled) of this contract"""
        return self.__logs.get()


class ContractFactory:
    """Factory (prototype) of a contract"""
    def __init__(self, w3: Web3, interface):
        self.__w3 = w3
        self.__interface = interface
        self.__contract_factory = self.__w3.eth.contract(**self.__interface)

    def deploy(self, *args, **kwargs):
        """Deploy a new instance of this contract"""
        tx_hash = self.__contract_factory.deploy(args=args, **kwargs)
        address = self.__w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return ContractInstance(self.__w3, address, self.__interface)
