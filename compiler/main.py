import os
import AST.grammar as grammar
import compiler.compiler_utils as compiler_utils
from Semantic.semantic import *


def main():
    prog = '''
str = "Hello"
name = input("Input name: ") // comment 
print(str, name)
a = 2
b = 3 + a
bool = a < b
factorial = 1

if a > 7 + b :  
    a = 7

while g2 > g :
    output(g2)  
    c = a+b * (2 - 1) + 0

for i in range(1, number + 1):
    factorial = factorial * i

def func(a):
    a = a * 3
    print(a + 5)

    '''

    prog = grammar.parse(compiler_utils.close_blocks(prog))
    print(*prog.tree, sep=os.linesep)
    symb_table_builder = SemanticAnalyzer()
    symb_table_builder.visit(prog)


if __name__ == "__main__":
    main()
