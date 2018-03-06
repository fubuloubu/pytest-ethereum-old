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
        tester.mine_blocks()  # mines an empty block

    timelimited.setExpired()
    # You can check to see if a contract still has code
    # NOTE: Implicitly calls address.codesize != 0
    assert timelimited.hascode
    timelimited.destroy()  # Calls selfdestruct opcode, removing code
    assert not timelimited.hascode
    
    # Get Ether balance of any address
    print("Account 0 has", tester.accounts[0].balance, "Wei")
    print("Account 1 has", tester.accounts[1].balance, "Wei")
    print("Contract 'timelimited' has", timelimited.balance, "Wei")

    # Send any address Ether
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
    return tester.contracts('path/to/Token.sol').deploy(*args)


def test_token(tester, Token):
    # You can do all of these with the your own fixtures too!

    # Test Token.transfer()
    assert Token.balanceOf(tester.accounts[0]) == INITIAL_SUPPLY
    assert Token.balanceOf(tester.accounts[1]) == 0
    Token.transfer(tester.accounts[1], 10)  # Creates a log
    assert Token.balanceOf(tester.accounts[0]) == INITIAL_SUPPLY - 10
    assert Token.balanceOf(tester.accounts[1]) == 10
    # Create a Transfer log to check against
    expected_log = Token.gen_log('Transfer',
            # Below is all the members of the event
            _from=tester.accounts[0],
            _to=tester.accounts[1],
            _value=10
        )
    # Test transfer's event against the expected value
    assert Token.new_logs[-1] == expected_log

    # Note: Contract.new_logs resets everytime it's polled
    assert len(Token.new_logs) == 0

    # You can also check individual fields
    Token.approve(tester.accounts[2], 10)
    Approval = Token.new_logs[-1]
    assert Approval['_owner'] == tester.accounts[0]
    assert Approval['_spender'] == tester.accounts[2]
    assert Approval['_value'] == 10

# Constants for ICO
TOKEN_PRICE = 1000  # 100 wei/token
HARDCAP = INITIAL_SUPPLY  # Max tokens for sale
SOFTCAP = 10  # Min tokens for successful sale
DURATION = 100  # active blocks

@pytest.fixture
def ICO(tester, Token):
    # If you need to link fixtures together, you can!
    args = [TOKEN_PRICE, HARDCAP, SOFTCAP, DURATION, Token.address]
    return tester.contracts('path/to/ICO.sol').deploy(*args)

import random
def test_ico(tester, Token, ICO):
    # NOTE: Token is not the same deployment as the one in test_token!
    assert Token.balanceOf(tester.accounts[0]) == INITIAL_SUPPLY

    # You can add accounts if you need to
    #tester.add_account()

    Token.approve(ICO.address, ICO.hardCap())
    ICO.startICO()  # Let's get this party started!

    # You can create very powerful tests with this library
    tp = ICO.tokenPrice()
    sold = 0  # use this later
    while not ICO.hardCapReached():
        # Every round, buyer buys an amount of tokens between [1, softCap)
        buyer = random.choice(tester.accounts[1:])
        amount = tp*min(random.randrange(1, ICO.softCap()),ICO.hardCap()-sold)
        ICO.buyToken(transact={'from':buyer, 'value':amount})
        print(buyer, "bought", ICO.sold()-sold, "tokens this round!")
        sold = ICO.sold()  # Update for next round
