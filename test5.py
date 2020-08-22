from machine import *

program = [
    'PUSH', 2,
    'PUSH', 8,
    'CALL', 10,
    'FUNC', 'print', 1,
    'HALT',
    'STORE', 'b',
    'STORE', 'a',
    'PUSH', 1,
    'STORE', 'result',
    'PUSH', 0,
    'STORE', 'i',
    'LOAD', 'b',
    'LOAD', 'i',
    'ISGT',
    'NOT',
    'JUMP_IF', 46,
    'LOAD', 'a',
    'LOAD', 'result',
    'MUL',
    'STORE', 'result',
    'LOAD', 'i',
    'PUSH', 1,
    'ADD',
    'STORE', 'i',
    'JUMP', 22,
    'LOAD', 'result',
    'RET'
]
instruction_table = Machine.get_instruction_table()

machine = Machine(program, instruction_table)
machine.run()
