from web3 import Web3


class Account:
    def __init__(self, w3: Web3, address):
        self._w3 = w3
        self._address = address

    def __repr__(self):
        return self._address

    def __str__(self):
        return self.__repr__()

    def __ne__(self, other):
        return self.__repr__().__ne__(other)

    def __eq__(self, other):
        return self.__repr__().__eq__(other)

    # Send Ether
    def send(self, address, amount):
        self._w3.eth.sendTransaction({'to': address, 'from': self._address, 'value': amount})

    @property
    def balance(self):
        return self._w3.getBalance(self._address)
