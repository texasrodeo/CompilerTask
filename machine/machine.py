from .instructionTable import InstructionTable
from .instruction import Instruction
from .context import Context
import builtins


class Machine:

    def __init__(self, program: list, instruction_table: InstructionTable):
        self.program = program
        self.instruction_table = instruction_table
        self.instruction_pointer = 0
        self.operand_stack = []
        self.context_stack = []
        self.current_context = Context(-1)
        self.context_stack.append(self.current_context)
        self._is_halted = False

    def push_operand(self, operand):
        self.operand_stack.insert(0, operand)

    def pop_operand(self):
        return self.operand_stack.pop(0)

    def push_context(self, return_address):
        self.current_context = Context(return_address)
        self.context_stack.insert(0, self.current_context)

    def pop_context(self):
        self.context_stack.pop(0)
        self.current_context = self.context_stack[0]

    def get_next_code(self):
        code = self.program[self.instruction_pointer]
        self.instruction_pointer += 1
        return code

    def run(self):
        while not self._is_halted:
            self.step()

    def step(self):
        op_name = self.get_next_code()
        instruction = self.instruction_table.get(op_name)
        if not instruction:
            raise Exception('Instruction ' + op_name + 'does not supported')

        args = []
        for i in range(instruction.arity):
            args.append(self.get_next_code())
        instruction.func(self, args)

    @classmethod
    def get_instruction_table(cls) -> InstructionTable:
        instruction_table = InstructionTable()
        instruction_table.insert(Instruction('HALT', 0, cls.halt))
        instruction_table.insert(Instruction('PUSH', 1, cls.push))
        instruction_table.insert(Instruction('POP', 0, cls.pop))
        instruction_table.insert(Instruction('DUP', 0, cls.dup))
        instruction_table.insert(Instruction('ADD', 0, cls.add))
        instruction_table.insert(Instruction('SUB', 0, cls.sub))
        instruction_table.insert(Instruction('MUL', 0, cls.mul))
        instruction_table.insert(Instruction('DIV', 0, cls.div))
        instruction_table.insert(Instruction('AND', 0, cls.and_op))
        instruction_table.insert(Instruction('OR', 0, cls.or_op))
        instruction_table.insert(Instruction('NOT', 0, cls.not_op))
        instruction_table.insert(Instruction('ISEQ', 0, cls.is_equal))
        instruction_table.insert(Instruction('ISGT', 0, cls.is_greater))
        instruction_table.insert(Instruction('ISGE', 0, cls.is_greater_equal))
        instruction_table.insert(Instruction('JUMP', 1, cls.jump))
        instruction_table.insert(Instruction('JUMP_IF', 1, cls.jump_if))
        instruction_table.insert(Instruction('LOAD', 1, cls.load))
        instruction_table.insert(Instruction('STORE', 1, cls.store))
        instruction_table.insert(Instruction('FUNC', 2, cls.call_builtin_func))
        instruction_table.insert(Instruction('CALL', 1, cls.call))
        instruction_table.insert(Instruction('RET', 0, cls.ret))
        return instruction_table

    def halt(self, args):
        self._is_halted = True

    def push(self, args):
        arg = args[0]
        self.push_operand(arg)

    def pop(self, args):
        self.pop_operand()

    def dup(self, args):
        op = self.pop_operand()
        self.push_operand(op)
        self.push_operand(op)

    def add(self, add):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh + rh)

    def sub(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh - rh)

    def mul(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh * rh)

    def div(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh / rh)

    def and_op(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh and rh)

    def or_op(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh or rh)

    def not_op(self, args):
        op = self.pop_operand()
        self.push_operand(not op)

    def is_equal(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh == rh)

    def is_greater(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh > rh)

    def is_greater_equal(self, args):
        rh = self.pop_operand()
        lh = self.pop_operand()
        self.push_operand(lh >= rh)

    def jump(self, args):
        new_ip = args[0]
        self.instruction_pointer = new_ip

    def jump_if(self, args):
        new_ip = args[0]
        condition = self.pop_operand()
        if condition:
            self.instruction_pointer = new_ip

    def print_op(self, args):
        print(self.pop_operand())

    def load(self, args):
        variable_name = args[0]
        variable = self.current_context.get_variable(variable_name)
        self.push_operand(variable)

    def store(self, args):
        variable_name = args[0]
        variable = self.pop_operand()
        self.current_context.set_variable(variable_name, variable)

    def call_builtin_func(self, args):
        func_name = args[0]
        argv = args[1]
        params = []
        for i in range(argv):
            params.append(self.pop_operand())
        func = getattr(builtins, func_name)
        self.push_operand(func(*params))

    def call(self, args):
        new_ip = args[0]
        self.push_context(self.instruction_pointer)
        self.instruction_pointer = new_ip

    def ret(self, args):
        new_ip = self.current_context.get_return_address()
        self.pop_context()
        self.instruction_pointer = new_ip
