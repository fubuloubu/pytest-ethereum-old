from web3 import Web3


class Account:
    def __init__(self, w3: Web3, address):
        self._w3 = w3
        self._address = address

    def __repr__(self):
        return self._address

    # Send Ether
    def send(self, address, amount):
        self._w3.eth.sendTransaction({'to': address, 'from': self._address, 'value': amount})

    @property
    def balance(self):
        return self._w3.getBalance(self._address)
