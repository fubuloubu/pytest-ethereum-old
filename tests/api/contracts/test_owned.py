import pytest


@pytest.fixture
def Owned(t):
    interface = {
        "bytecode":
            "0x6060604052336000806101000a81548173ffffffffffffffffffffffffffffff"
            "ffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602"
            "17905550341561004f57600080fd5b6101ce8061005e6000396000f30060606040"
            "526004361061004c576000357c0100000000000000000000000000000000000000"
            "000000000000000000900463ffffffff1680638da5cb5b14610051578063a6f9da"
            "e1146100a6575b600080fd5b341561005c57600080fd5b6100646100df565b6040"
            "51808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffff"
            "ffffffffffffffffffffffffff16815260200191505060405180910390f35b3415"
            "6100b157600080fd5b6100dd600480803573ffffffffffffffffffffffffffffff"
            "ffffffffff16906020019091905050610104565b005b6000809054906101000a90"
            "0473ffffffffffffffffffffffffffffffffffffffff1681565b60008090549061"
            "01000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffff"
            "ffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffff"
            "ffffffffff1614151561015f57600080fd5b806000806101000a81548173ffffff"
            "ffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffff"
            "ffffffffffffffffffff160217905550505600a165627a7a72305820880a4056fa"
            "b249ea33a384814995ed65839292e7edf737e2082462ab370b372a0029",
        "bytecode_runtime":
            "0x60606040526004361061004c576000357c010000000000000000000000000000"
            "0000000000000000000000000000900463ffffffff1680638da5cb5b1461005157"
            "8063a6f9dae1146100a6575b600080fd5b341561005c57600080fd5b6100646100"
            "df565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffff"
            "ffffffffffffffffffffffffffffffffffff168152602001915050604051809103"
            "90f35b34156100b157600080fd5b6100dd600480803573ffffffffffffffffffff"
            "ffffffffffffffffffff16906020019091905050610104565b005b600080905490"
            "6101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000"
            "809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673"
            "ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffff"
            "ffffffffffffffffffff1614151561015f57600080fd5b806000806101000a8154"
            "8173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffff"
            "ffffffffffffffffffffffffffffff160217905550505600a165627a7a72305820"
            "880a4056fab249ea33a384814995ed65839292e7edf737e2082462ab370b372a00"
            "29",
        "abi": [
            {
                "constant": True,
                "inputs": [],
                "name":"owner",
                "outputs":[
                    {
                        "name": "",
                        "type": "address"
                    }
                ],
                "payable": False,
                "stateMutability": "view",
                "type": "function"
            },
            {
                "constant": False,
                "inputs":[
                    {
                        "name": "newOwner",
                        "type": "address"
                    }
                ],
                "name": "changeOwner",
                "outputs": [],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
    }
    #return t.new_contract(interface)()
    return t.c('path/to/Owned.sol')()

def test_transfer_ownership(t, Owned):
    assert Owned.owner() == t.a[0]
    with t.tx_fails:
        Owned.changeOwner(t.a[1], transact={'from': t.a[1]})
    Owned.changeOwner(t.a[1], transact={'from': t.a[0]})
    assert Owned.owner() == t.a[1]
    with t.tx_fails:
        Owned.changeOwner(t.a[2], transact={'from': t.a[0]})
    Owned.changeOwner(t.a[0], transact={'from': t.a[1]})
    assert Owned.owner() == t.a[0]
