import json
from os.path import isfile as file_exists


def get_assets(filename='../contracts/contracts.json'):
    if file_exists(filename):
        with open(filename, 'r') as f:
            compiled_interfaces = json.loads(f.read())['contracts']
        # check proper structure e.g.
        # 'Contract1' : { 'abi' : ..., 'bytecode' : ..., 'bytecode_runtime' : ... }, 'Contract2' : ...
        required_members = ['abi', 'bytecode', 'bytecode_runtime']
        for name, interface in compiled_interfaces.items():
            filtered_interface = dict()
            for member in interface.keys():
                # Conversions for unique outputs
                if member == 'abi':
                    filtered_interface['abi'] = interface[member]
                if member == 'bin':
                    filtered_interface['bytecode'] = interface[member]
                if member == 'bin-runtime':
                    filtered_interface['bytecode_runtime'] = interface[member]
            for member in required_members:
                assert member in filtered_interface.keys(), "Contract '{}' doesn't have '{}'!".format(name, member)
            compiled_interfaces[name] = filtered_interface
    else:
        compiled_interfaces = None
    return compiled_interfaces
