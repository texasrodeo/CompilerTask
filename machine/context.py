class Context:

    def __init__(self, return_address):
        self.variables = dict()
        self.return_address = return_address

    def get_return_address(self):
        return self.return_address

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables[name]
