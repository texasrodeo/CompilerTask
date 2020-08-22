

class Instruction:

    def __init__(self, name: str, arity: int, func):
        self.name = name
        self.arity = arity
        self.func = func
