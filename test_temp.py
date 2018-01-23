# Fixtures provided:
# t: EthereumTester instance
# contract_tester: fixture to generate Contract instances for testing
# tx_fails: fixture to help with 'TransactionFailed' test cases

# Fixtures generated:
# Anything defined using the '!fixture' parse tag in config.yml
# (must have deployment arguments defined)
# e.g. Token

def test_stuff(t, contract_tester, tx_fails, Token):
    
    # Get contract via name from 'contracts.json' file (output of Solidity)
    # NOTE path to this file set in config.yml
    c1 = contract_tester(contract='utils/Owned.sol')
    
    # You can specify a specific contract in the file (assumes file basename by default)
    # You must specify the deployment args
    c2 = contract_tester(contract='utils/TimeLimited.sol:TestTimeLimited', args=[10])

    # You can also load a contract ad-hoc via a contract interface
    # Requires interface={'abi': [...], 'bytecode': '0x...', 'bytecode_runtime': '0x...'}
    adhoc_interface = {'abi': [], 'bytecode': '0x0', 'bytecode_runtime': '0x0'}
    # Can supply transact={...} to change deployment transaction params
    c3 = contract_tester(interface=adhoc_interface, transact={'from': t.a1})

    # Use normal assert syntax for testing
    # 'constant' functions call by default
    assert c1.owner() == t.a0
    # non-'constant' functions transact by default
    # NOTE: Transactions auto-mine (see eth-tester)
    c1.changeOwner(t.a1)
    assert c1.owner() == t.a1
    # Use this for asserting a failed transaction should occur
    with tx_fails:
        c1.changeOwner(t.a0)
    
    # You can supply optional transaction params
    c1.changeOwner(t.a0, transact={'from':t.a1})
    assert c1.owner() == t.a0
    
    # You can mine a block
    while c2.alive():
        t.mine_block()

    c2.setExpired()
    # You can check to see if a contract still has code
    assert t.hascode(c2.address)
    c2.destroy()  # Calls selfdestruct opcode
    assert not t.hascode(c2.address)

    # You can do all of these with the generated fixtures too!
    assert Token.balanceOf(t.a0) >= 100
    assert Token.balanceOf(t.a1) == 0
    Token.transfer(t.a1, 100)
    assert Token.balanceOf(t.a1) == 100
    # All contracts (generated or ad-hoc) have an address
    print("Token's address:", Token.address)
    # Get Ether balance of any address
    print(t.get_balance(t.a0), "Wei")
    print(t.get_balance(Token.address), "Wei")
