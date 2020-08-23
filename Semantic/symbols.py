class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name


class BlockSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return '{name}'.format(name=self.name)
