class Log:
    def __init__(self, _log):
        self._event = _log['event']
        self._args = _log['args']

    def __eq__(self, other):
        if not isinstance(other, Log):
            return False
        if self._event != other._event:
            return False
        for k, v in self._args.items():
            if v != other._args[k]:
                return False
        return True

    def __getitem__(self, key):
        #TODO Throw if key not in _args
        return self._args[key]

    def __repr__(self):
        args = map(lambda a: "'{}': '{}'".format(*a), self._args.items())
        return self._event + '(' + ', '.join(args) + ')'
