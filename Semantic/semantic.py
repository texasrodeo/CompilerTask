from AST.grammar import *
from Semantic.symbols import *


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class ScopedSymbolTable(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.init_builtins()

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
                ('Enclosing scope',
                 self.enclosing_scope.scope_name if self.enclosing_scope else None
                )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, str(value)))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    def init_builtins(self):
        self.define(BuiltinTypeSymbol('integer'))
        self.define(BuiltinTypeSymbol('char'))

    def define(self, symbol: Symbol):
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False) -> Symbol:
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_BinOpNode(self, node):
        self.visit(node.arg1)
        self.visit(node.arg2)

    def visit_IdentNode(self, node: IdentNode):
        var_name = node.name

    def visit_LiteralNode(self, node: LiteralNode):
        pass

    def visit_StmtListNode(self, node: StmtListNode):
        for stmt in node.exprs:
            self.visit(stmt)

    def visit_AssignNode(self, node: AssignNode):
        var_name = node.var.name
        self.visit(node.val)

    def visit_CallNode(self, node: CallNode):
        for param in node.params:
            self.visit(param)

    def visit_IfNode(self, node: IfNode):
        self.visit(node.cond)
        self.visit(node.then_stmt)

        if node.else_stmt:
            self.visit(node.else_stmt)

    def visit_WhileNode(self, node: WhileNode):
        self.visit(node.cond)
        self.visit(node.stmt)

    def visit_DefNode(self, node: DefNode):
        self.visit(node.def_name)
        self.visit(node.args)
        self.visit(node.stmt)

    def visit_ForNode(self, node: ForNode):
        self.visit(node.init)
        self.visit(node.for_in)
        self.visit(node.body)
