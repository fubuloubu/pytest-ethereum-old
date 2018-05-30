def test_init(t):
    for acct in t.accounts:
        assert acct.balance > 0
        assert acct not in filter(lambda a: a != acct, t.accounts)

def test_transfer(t):
    """
    Ether transfers work
    """
    starting_balance = t.a[0].balance
    assert t.a[1].balance == starting_balance

    t.a[0].transfer(t.a[1], 100)
    assert t.a[0].balance == starting_balance - 100
    assert t.a[1].balance == starting_balance + 100
    
    t.a[1].transfer(t.a[0], 100)
    assert t.a[0].balance == t.a[1].balance == starting_balance
