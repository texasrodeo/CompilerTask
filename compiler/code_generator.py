import inspect
from typing import List
from pyparsing import ParseResults
from AST.nodes import *
import compiler.custom_builtins as custom_builtins
op_cmd = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
    '%': 'MOD',
    '>=': 'GE',
    '<=': 'LE',
    '!=': 'NEQ',
    '==': 'EQ',
    '>': 'GT',
    '<': 'LT',
    '&&': 'AND',
    '||': 'OR',
    '**': 'PWR'
}
builtin_funcs = [f for f in dir(custom_builtins) if inspect.isfunction(getattr(custom_builtins, f))]

class CodeLine:
    def __init__(self, cmd: str, value: Optional = None):
        self.cmd = cmd
        self.value = value

    def __str__(self):
        return self.cmd + ' ' + (str(self.value) if self.value is not None else '')

class CodeGenerator:
    def __init__(self, ast: StmtNode):
        self.__ast = ast
        self.lines: List[CodeLine] = []
        self.__funcs = {}
        self.__compile_functions()
        self.__generate_code(self.__ast)
        self.__add_line(CodeLine('HALT'))

    def __compile_functions(self):
        for child in self.__ast.children:
            if child.__class__.__name__ in ["FuncDeclarationNode"]:
                self.__funcs[child.ident.name] = len(self.lines) + 1
                if not isinstance(child.params.params[0], ParseResults):
                    for param in child.params.params[::-1]:
                        self.__add_line(CodeLine('STORE', param.name))
                self.__generate_code(child.block)
                if self.lines[len(self.lines) - 1].cmd not in ['RET']:
                    self.__add_line(CodeLine('RET'))
        if len(self.__funcs) != 0:
            self.__add_line_at(CodeLine('JMP', len(self.lines) + 1), 0, len(self.lines))

    def __generate_code(self, node: AstNode):
        if node.__class__.__name__ in ["BinExprNode"]:
            self.__compile_binexpr(node)
        elif node.__class__.__name__ in ["UnaryExprNode"]:
            self.__compile_unexpr(node)
        elif node.__class__.__name__ in ["LiteralNode"]:
            self.__add_line(CodeLine('PUSH', node.value))
        elif node.__class__.__name__ in ["IdentNode"]:
            self.__add_line(CodeLine('LOAD', node.name))
        elif node.__class__.__name__ in ["ReturnNode"]:
            self.__generate_code(node.argument)
            self.__add_line(CodeLine('RET'))
        elif node.__class__.__name__ in ["DeclaratorNode"]:
            if node.init is not None:
                self.__generate_code(node.init)
                self.__add_line(CodeLine('STORE', node.ident.name))
        elif node.__class__.__name__ in ["CallNode"]:
            for param in node.args:
                self.__generate_code(param)
            if node.ident.name in builtin_funcs:
                self.__add_line(CodeLine('CBLTN', node.ident.name))
            else:
                self.__add_line(CodeLine('CALL', self.__funcs[node.ident.name]))
        elif node.__class__.__name__ in ["BlockStatementNode", "VarDeclarationNode"]:
            for child in node.children:
                self.__generate_code(child)
        elif node.__class__.__name__ in ["IfNode"]:
            self.__compile_if(node)
        elif node.__class__.__name__ in ["WhileNode"]:
            self.__compile_while(node)
        elif node.__class__.__name__ in ["DoWhileNode"]:
            self.__compile_dowhile(node)
        elif node.__class__.__name__ in ["ForNode"]:
            self.__compile_for(node)