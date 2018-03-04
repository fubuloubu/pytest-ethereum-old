from web3 import Web3


class ContractInstance:
    def __init__(self, w3: Web3, address, interface):
        self.__w3 = w3
        self.__address = address
        self.__instance = self.__w3.eth.contract(self.__address, **interface,
                ContractFactoryClass=ImplicitContract)
        # Register new filter to watch for logs from this instance's address
        self.__filter = self.__w3.eth.filter({'address': self.__address})
        self.__logs = self.__w3.utils.filters.LogFilter(self.__filter)

    @property
    def address(self):
        return self.__address

    @property
    def balance(self):
        return self.__w3.eth.getBalance(self.address)

    @property
    def codesize(self):
        return len(self.__w3.eth.getCode(self.address)[2:])/2

    @property
    def hascode(self):
        return self.codesize != 0

    @property
    def logs(self):
        # Returns all the event logs created (since last polled)
        return self.__logs.get()


class ContractFactory:
    def __init__(self, w3: Web3, interface):
        self.__w3 = w3
        self.__interface
        self.__contract_factory = self.__w3.eth.contract(**interface)

    def deploy(self, **kwargs):
        tx_hash = self.__contract_factory.deploy(**kwargs)
        address = self.__w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return ContractInstance(self.__w3, address, self.__interface)
