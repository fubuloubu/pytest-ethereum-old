from eth_utils import event_abi_to_log_topic
from web3.utils.events import get_event_data
from functools import partial as partial_fn


def clean_modifiers(modifiers):
    cleaned_modifiers = modifiers.copy()
    for name, modifier in modifiers.items():
        for key, value in modifier.items():
            if not isinstance(value, str) or not isinstance(value, int):
                cleaned_modifiers[name][key] = str(value)
    return cleaned_modifiers


def get_event_signatures(abi_list):
    signatures = dict()
    for abi in abi_list:
        if abi['type'] == 'event':
            signatures[abi['name']] = event_abi_to_log_topic(abi)
    return signatures


def get_event_processors(abi_list):
    processors = dict()
    for abi in abi_list:
        if abi['type'] == 'event':
            processors[event_abi_to_log_topic(abi)] = partial_fn(get_event_data, abi)
    return processors
