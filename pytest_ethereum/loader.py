# Constants related to the platform
import yaml

# Override behavior for testing (vs deployments)
def testing_deployment(l, n):
    mapping = l.construct_mapping(n)
    # Encode all strings as bytes
    for key, value in mapping.items():
        if isinstance(value, str):
            mapping[key] = bytes(value, 'utf-8')
    return mapping
yaml.add_constructor('!fixture', testing_deployment)

import os
path = os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(path + '/' + './fixtures.yml')
with open(path, 'r') as f:
    constants = yaml.load(f.read())
