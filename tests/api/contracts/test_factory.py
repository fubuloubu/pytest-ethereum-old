from hexbytes import HexBytes

def test_CreateFactoryFromInterface(t):
    _interface = {'abi': [], 'bytecode': '0x', 'bytecode_runtime': '0x'}
    # Factory class has the same interface that we gave it
    # NOTE: Names are changed to work with Web3.py API
    _factory = t.new_contract(_interface)
    assert _factory.abi == _interface['abi']
    assert _factory.bytecode == HexBytes(_interface['bytecode'])
    assert _factory.bytecode_runtime == HexBytes(_interface['bytecode_runtime'])
    # Factory instances are unique
    assert _factory() is not _factory()
