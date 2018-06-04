import pytest


@pytest.fixture
def Faucet(t):
    interface = {
        "bytecode":
            "0x608060405234801561001057600080fd5b5060e08061001f6000396000f3006"
            "08060405260043610603f576000357c0100000000000000000000000000000000"
            "000000000000000000000000900463ffffffff1680632e1a7d4d146041575b005"
            "b348015604c57600080fd5b506069600480360381019080803590602001909291"
            "90505050606b565b005b3373ffffffffffffffffffffffffffffffffffffffff1"
            "66108fc829081150290604051600060405180830381858888f193505050501580"
            "1560b0573d6000803e3d6000fd5b50505600a165627a7a72305820672298c662a"
            "abd49d65f686862bea2edb3b885edf4605abaab6124a2a2d58f090029",
        "bytecode_runtime":
            "0x608060405260043610603f576000357c0100000000000000000000000000000"
            "000000000000000000000000000900463ffffffff1680632e1a7d4d146041575b"
            "005b348015604c57600080fd5b506069600480360381019080803590602001909"
            "29190505050606b565b005b3373ffffffffffffffffffffffffffffffffffffff"
            "ff166108fc829081150290604051600060405180830381858888f193505050501"
            "5801560b0573d6000803e3d6000fd5b50505600a165627a7a72305820672298c6"
            "62aabd49d65f686862bea2edb3b885edf4605abaab6124a2a2d58f090029",
        "abi": [
                {
                    "constant":False,
                    "inputs":[{"name":"amount","type":"uint256"}],
                    "name":"withdraw",
                    "outputs":[],
                    "payable":False,
                    "stateMutability":"nonpayable",
                    "type":"function"
                },
                {
                    "payable":True,
                    "stateMutability":"payable",
                    "type":"fallback"
                }
            ]
        }
    return t.new_contract(interface)()


def test_transfer(t, Faucet):
    starting_balance = t.a[0].balance
    assert Faucet.balance == 0
    t.a[0].transfer(Faucet.address, 100)
    assert t.a[0].balance == starting_balance - 100
    assert Faucet.balance == 100
    Faucet.withdraw(100)
    assert Faucet.balance == 0
    assert t.a[0].balance == starting_balance
