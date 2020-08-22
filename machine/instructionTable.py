from .instruction import Instruction


class InstructionTable:

    def __init__(self):
        self.table = {}

    def insert(self, instruction: Instruction):
        self.table[instruction.name] = instruction

    def get(self, name: str) -> Instruction:
        return self.table[name]
