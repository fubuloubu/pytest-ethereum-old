from web3 import Web3


class Account(str):
    def __new__(cls, w3: Web3, address):
        obj = super().__new__(cls, address)
        obj._w3 = w3
        obj._address = address
        return obj

    # Send Ether
    def send(self, address, amount):
        self._w3.eth.sendTransaction({'to': address, 'from': self._address, 'value': amount})

    @property
    def balance(self):
        return self._w3.eth.getBalance(self._address)
