import json
from os.path import isfile as file_exists


def load_package(filename):

    assert file_exists(filename), \
            "Filename '{}' doesn't exist!".format(filename)
    with open(filename, 'r') as f:
        compiled_interfaces = json.loads(f.read())['contracts']
    
    # compiled JSON package object should be structured like:
    # 'contracts' : {
    #   'Contract1' : {
    #           'abi' : ..., 
    #           'bytecode' : ..., 
    #           'bytecode_runtime' : ... 
    #   },
    #   'Contract2' : ...
    # }
    required_members = ['abi', 'bytecode', 'bytecode_runtime']

    for name, interface in compiled_interfaces.items():
        # Filter out stuff we don't need
        filtered_interface = dict()
        for member in interface.keys():
            if member == 'abi':
                abi = interface[member]
                if isinstance(abi, str):
                    abi = json.loads(abi)  # No idea why solidity does this...
                filtered_interface['abi'] = abi
            # Standardize names to Web3.py expected interfaces
            if member == 'bin' or member == 'bytecode':
                filtered_interface['bytecode'] = interface[member]
            if member == 'bin-runtime' or member == 'bytecode_runtime':
                filtered_interface['bytecode_runtime'] = interface[member]

        # Check for required interfaces
        for member in required_members:
            assert member in filtered_interface.keys(), \
                    "Contract '{}' doesn't have '{}'!".format(name, member)

        # Result is now exactly what we were looking for
        compiled_interfaces[name] = filtered_interface
    
    return compiled_interfaces
