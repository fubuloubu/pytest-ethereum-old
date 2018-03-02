# Fixtures provided:
# tester: web3.EthereumTester instance
#   .contracts: fixture to retreive Contract instances from assets file
#   .new_contract: fixture to generate new Contract instances
#   .tx_fails: fixture to help with 'TransactionFailed' test cases
def test_stuff(tester, Token):

    # Get contracts via name from 'contracts.json' file
    # NOTE: When no contract is selected, uses file basename (e.g. 'Owned')
    c1 = tester.contracts('path/to/Owned.sol').deploy()
    
    # You can specify a specific contract from the file
    TestContract = tester.contracts('path/to/TimeLimited.sol:TestTimeLimited')
    # You must specify the deployment args, supplied as an ordered list
    c2 = TestContract.deploy(args=[10])

    # You can also load and deploy a contract ad-hoc via a contract interface
    # Requires interface={'abi': [...], 'bytecode': '0x...', 'bytecode_runtime': '0x...'}
    adhoc_interface = {'abi': [], 'bytecode': '0x0', 'bytecode_runtime': '0x0'}
    ad_hoc = tester.new_contract(adhoc_interface)
    
    # You can deploy it multiple times
    one = ad_hoc.deploy()
    another = ad_hoc.deploy()
    
    # Can supply transact={...} to change deployment transaction params
    c3 = ad_hoc.deploy(transact={'from': tester.account[1]})

    # Use normal assert syntax for testing
    # 'constant' functions call by default
    assert c1.owner() == tester.account[0]
    
    # non-'constant' functions transact by default
    # NOTE: Transactions auto-mine (see eth-tester)
    c1.changeOwner(tester.account[1])
    assert c1.owner() == tester.account[1]
    
    # Use this for asserting a failed transaction should occur
    with tester.tx_fails:
        c1.changeOwner(tester.account[0])
    
    # You can supply optional transaction params
    c1.changeOwner(tester.account[0], transact={'from': tester.account[1]})
    assert c1.owner() == tester.account[0]
    
    # You can mine a block
    while c2.alive():
        tester.mine_block()

    c2.setExpired()
    # You can check to see if a contract still has code
    assert tester.hascode(c2.address)
    c2.destroy()  # Calls selfdestruct opcode
    assert not tester.hascode(c2.address)


# Create your own fixtures
import pytest
@pytest.fixture
def Token(tester):
    return tester.contracts('path/to/Token.sol:Token').deploy()

def test_token(tester, Token):
    # You can do all of these with the your own fixtures too!
    assert Token.balanceOf(tester.account[0]) >= 100
    assert Token.balanceOf(tester.account[1]) == 0
    Token.transfer(tester.account[1], 100)
    assert Token.balanceOf(tester.account[1]) == 100
    
    # All contracts (generated or ad-hoc) have an address
    print("Token's address:", Token.address)
    
    # Get Ether balance of any address
    print(tester.get_balance(tester.account[0]), "Wei")

    # Send any address Ether
    tester.account[1].send(Token.address, 100)  # send 100 wei
    print(tester.get_balance(Token.address), "Wei")
