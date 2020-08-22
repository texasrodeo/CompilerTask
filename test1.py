from machine import *

program = [
    'PUSH', 3,
    'PUSH', 8,
    'MUL',
    'PUSH', 10,
    'PUSH', 8,
    'PUSH', 2,
    'DIV',
    'SUB',
    'PUSH', 3,
    'MUL',
    'ADD',
    'FUNC', 'print', 1,
    'HALT'
]

instruction_table = Machine.get_instruction_table()

machine = Machine(program, instruction_table)
machine.run()
