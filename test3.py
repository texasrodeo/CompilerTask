from machine import *

program = [
    'PUSH', 100,
    'STORE', 'a',
    'PUSH', 30,
    'STORE', 'b',
    'LOAD', 'a',
    'LOAD', 'b',
    'ISGT',
    'JUMP_IF', 21,
    'LOAD', 'b',
    'STORE', 'c',
    'JUMP', 25,
    'LOAD', 'a',
    'STORE', 'c',
    'LOAD', 'c',
    'FUNC', 'print', 1,
    'HALT'
]
instruction_table = Machine.get_instruction_table()

machine = Machine(program, instruction_table)
machine.run()
