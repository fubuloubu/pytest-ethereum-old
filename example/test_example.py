# Just use the 'tester' fixture in your pytest_ethereum-enabled tests
def test_stuff(tester):

    # Get contracts via name from your assets file (e.g. 'contracts.json')
    # NOTE: When no contract from file is selected,
    #       uses file basename e.g. 'path/to/Owned.sol:Owned'
    owned = tester.contracts('path/to/Owned.sol').deploy()
    
    # You can specify a specific contract from the file
    timelimited_factory = tester.contracts('path/to/TimeLimited.sol:TestTimeLimited')
    # You must specify the deployment args if they exist
    # NOTE: must be supplied in abi order
    timelimited = timelimited_factory.deploy(10)  # arg1: 10 blocks

    # You can also load and deploy a contract ad-hoc via a contract interface
    # Requires interface={'abi': [...], 'bytecode': '0x...', 'bytecode_runtime': '0x...'}
    adhoc_interface = {'abi': [], 'bytecode': '0x0', 'bytecode_runtime': '0x0'}
    ad_hoc_factory = tester.new_contract(adhoc_interface)
    
    # You can deploy from any contract factory multiple times
    one = ad_hoc_factory.deploy()
    another = ad_hoc_factory.deploy()
    
    # Can supply transact={...} to change deployment transaction params
    ad_hoc_a1 = ad_hoc_factory.deploy(transact={'from': tester.accounts[1]})
    
    # All contracts (generated or ad-hoc) have an address
    print("Ad-Hoc Adress is:", ad_hoc_a1.address)

    # Use normal assert syntax for testing
    # pure/view/constant functions call by default
    assert owned.owner() == tester.accounts[0]  # Doesn't mine a block!
    
    # non-'constant' functions transact by default
    # NOTE: Transactions auto-mine (see eth-tester)
    owned.changeOwner(tester.accounts[1])  # Transaction auto-mined into block
    assert owned.owner() == tester.accounts[1]  # No transaction here
    
    # Use this for asserting when a failed transaction should occur
    with tester.tx_fails:
        owned.changeOwner(tester.accounts[0])  # account 0 is no longer the owner!
    
    # You can supply optional transaction params
    owned.changeOwner(tester.accounts[0],
            transact={
                'from': tester.accounts[1],  # from a different sender
                #'value': 100,  # send 100 wei in this transaction
                # You can also do other things... see web3.py for more info!
            }
        )
    assert owned.owner() == tester.accounts[0]  # account[0] is the owner again!
    
    # You can mine an empty block if you want
    while timelimited.alive():  # This makes a call, so no transaction occurs
        tester.mine_block()  # mines an empty block

    timelimited.setExpired()
    # You can check to see if a contract still has code
    # NOTE: Implicitly calls address.codesize != 0
    assert timelimited.hascode
    timelimited.destroy()  # Calls selfdestruct opcode, removing code
    assert not timelimited.hascode
    
    # Get Ether balance of any address
    print("Account 0 has", tester.accounts[0].balance, "Wei")
    print("Account 1 has", tester.accounts[1].balance, "Wei")
    print("Contract 'timelimited' has", timelimited.address.balance, "Wei")

    # Send any address Ether
    print(tester.get_balance(tester.accounts[2]), "Wei")
    print("Account 2 has", tester.accounts[2].balance, "Wei")
    tester.accounts[1].send(tester.accounts[2], 100)  # send 100 wei to address 2
    print("Account 2 now has", tester.accounts[2].balance, "Wei")


import pytest


# Constants for Token
SYMBOL = 'TEST'
NAME = 'Test Token'
DECIMALS = 0
INITIAL_SUPPLY = 100

# You can also create your own fixtures!
@pytest.fixture
def Token(tester):
    args = [SYMBOL, NAME, DECIMALS, INITIAL_SUPPLY]  # for convienence
    token = tester.contracts('path/to/Token.sol').deploy(*args)  
    print("Token deployed at", token.address)
    return token


def test_token(tester, Token):
    # You can do all of these with the your own fixtures too!
    assert Token.balanceOf(tester.accounts[0]) == INITIAL_SUPPLY
    assert Token.balanceOf(tester.accounts[1]) == 0
    Token.transfer(tester.accounts[1], INITIAL_SUPPLY)
    assert Token.balanceOf(tester.accounts[1]) == INITIAL_SUPPLY
    Transfer
    Approval

# Constants for ICO
TOKEN_PRICE = 100  # 100 wei/token
HARDCAP = INITIAL_SUPPLY  # Max tokens for sale
SOFTCAP = 10  # Min tokens for successful sale
DURATION = 10  # active blocks

@pytest.fixture
def ICO(tester, Token):
    # If you need to link fixtures together, you can!
    args = [TOKEN_PRICE, HARDCAP, SOFTCAP, DURATION, Token.address]
    return tester.contracts('path/to/ICO.sol').deploy(*args)


def test_ico(tester, Token, ICO):
    # NOTE: Token is not the same deployment as the one in test_token!
    assert Token.balanceOf(tester.accounts[0]) == INITIAL_SUPPLY
    TokenBuy
    TokenRefund
