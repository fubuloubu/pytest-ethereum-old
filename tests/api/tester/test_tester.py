def test_mining(t):
    """
    Mining blocks works
    """
    starting_block = t.eth.blockNumber
    # Mining a block mines exactly one block
    t.mine_blocks()
    assert t.eth.blockNumber == starting_block + 1
    # Mining N blocks mines exactly N blocks
    t.mine_blocks(10)
    assert t.eth.blockNumber == starting_block + 11


def test_time(t):
    """
    t.now() gets the current time
    This should match the mined block time
    when the block is mined
    """
    # Check pending block time is returned
    # NOTE: pending block time is at creation
    start_time = t.now()
    start_block = t.eth.getBlock('pending')['number']
    assert start_time == t.now()  # Returns the same number if no mining
    # Mine a block, timestamps should match
    t.mine_blocks()
    assert t.eth.getBlock('latest')['timestamp'] == start_time
    assert t.now() > start_time
    # Mine another block, timestamps should still match
    t.mine_blocks()
    assert t.eth.getBlock(start_block)['timestamp'] == start_time


from eth_tester.exceptions import TransactionFailed


def test_exception(t):
    """
    Can call as many transaction failures in a row as you need
    """
    failures = 0
    with t.tx_fails:
        raise TransactionFailed
    failures += 1
    with t.tx_fails:
        raise TransactionFailed
    failures += 1
    with t.tx_fails:
        raise TransactionFailed
    failures += 1
    assert failures == 3
