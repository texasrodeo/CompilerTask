from machine import *

program = [
    'PUSH', 16,
    'STORE', 'a',
    'PUSH', 10,
    'STORE', 'b',
    'LOAD', 'a',
    'LOAD', 'b',
    'ISGT',
    'NOT',
    'JUMP_IF', 30,
    'LOAD', 'a',
    'PUSH', 1,
    'SUB',
    'STORE', 'a',
    'LOAD', 'a',
    'FUNC', 'print', 1,
    'JUMP', 8,
    'HALT'
]
instruction_table = Machine.get_instruction_table()

machine = Machine(program, instruction_table)
machine.run()
