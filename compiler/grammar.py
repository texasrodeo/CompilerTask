from contextlib import suppress

import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from compiler.nodes import *


def _make_parser():
    pp.ParserElement.setDefaultWhitespaceChars(' \t')
    num = pp.Regex('[+-]?\\d+\\.?\\d*([eE][+-]?\\d+)?')
    str_ = pp.QuotedString('"', escChar='\\', unquoteResults=False, convertWhitespaceEscapes=False)
    literal = num | str_
    ident = ppc.identifier.setName('ident')

    LPAR, RPAR = pp.Literal('(').suppress(), pp.Literal(')').suppress()
    LBRACK, RBRACK = pp.Literal("[").suppress(), pp.Literal("]").suppress()
    LBRACE, RBRACE = pp.Literal("{").suppress(), pp.Literal("}").suppress()
    SEMI, COMMA = pp.lineEnd().suppress(), pp.Literal(',').suppress()
    ASSIGN = pp.Literal('=')

    DOT = pp.Literal('.')
    ADD, SUB = pp.Literal('+'), pp.Literal('-')
    MUL, DIV = pp.Literal('*'), pp.Literal('/')
    AND = pp.Literal('&&')
    OR = pp.Literal('||')
    BIT_AND = pp.Literal('&')
    BIT_OR = pp.Literal('|')
    GE, LE, GT, LT = pp.Literal('>='), pp.Literal('<='), pp.Literal('>'), pp.Literal('<')
    NEQUALS, EQUALS = pp.Literal('!='), pp.Literal('==')

    expr = pp.Forward()
    stmt = pp.Forward()
    stmt_list = pp.Forward()

    call = ident + LPAR + pp.Optional(expr + pp.ZeroOrMore(COMMA + expr)) + RPAR

    group = (
        literal |
        call |
        ident |
        LPAR + expr + RPAR
    )

    mult = pp.Group(group + pp.ZeroOrMore((MUL | DIV) + group)).setName('bin_op')
    add = pp.Group(mult + pp.ZeroOrMore((ADD | SUB) + mult)).setName('bin_op')
    compare1 = pp.Group(add + pp.Optional((GE | LE | GT | LT) + add)).setName('bin_op')
    compare2 = pp.Group(compare1 + pp.Optional((EQUALS | NEQUALS) + compare1)).setName('bin_op')
    logical_and = pp.Group(compare2 + pp.ZeroOrMore(AND + compare2)).setName('bin_op')
    logical_or = pp.Group(logical_and + pp.ZeroOrMore(OR + logical_and)).setName('bin_op')

    expr << (logical_or)

    simple_assign = (ident + ASSIGN.suppress() + (expr | str_)).setName('assign')
    var_decl_inner = simple_assign | ident
    vars_decl = var_decl_inner + pp.ZeroOrMore(COMMA + var_decl_inner)

    assign = ident + ASSIGN.suppress() + expr
    simple_stmt = assign | call

    for_cond = ident + pp.Keyword("in").suppress() + call

    if_ = pp.Keyword("if").suppress() + expr + pp.Keyword(":").suppress() + stmt_list + RBRACE
    for_ = pp.Keyword("for").suppress() + for_cond + pp.Keyword(":").suppress() + stmt_list + RBRACE
    while_ = pp.Keyword("while").suppress() + expr + pp.Keyword(":").suppress() + stmt_list + RBRACE
    def_ = pp.Keyword("def").suppress() + ident + LPAR + pp.Optional(ident + pp.ZeroOrMore(COMMA.suppress() + ident))\
           + RPAR + pp.Keyword(":").suppress() + stmt_list + RBRACE

    stmt << (
            if_ |
            for_ |
            while_ |
            def_ |
            simple_stmt
    )

    stmt_list << (pp.ZeroOrMore(stmt + pp.ZeroOrMore(SEMI)))

    program = stmt_list.ignore(pp.cStyleComment).ignore(pp.dblSlashComment) + pp.StringEnd()

    start = program

    def set_parse_action_magic(rule_name: str, parser: pp.ParserElement)->None:
        if rule_name == rule_name.upper():
            return
        if getattr(parser, 'name', None) and parser.name.isidentifier():
            rule_name = parser.name
        if rule_name in ('bin_op', ):
            def bin_op_parse_action(s, loc, tocs):
                node = tocs[0]
                if not isinstance(node, AstNode):
                    node = bin_op_parse_action(s, loc, node)
                for i in range(1, len(tocs) - 1, 2):
                    secondNode = tocs[i + 1]
                    if not isinstance(secondNode, AstNode):
                        secondNode = bin_op_parse_action(s, loc, secondNode)
                    node = BinOpNode(BinOp(tocs[i]), node, secondNode)
                return node
            parser.setParseAction(bin_op_parse_action)
        else:
            cls = ''.join(x.capitalize() for x in rule_name.split('_')) + 'Node'
            with suppress(NameError):
                cls = eval(cls)
                if not inspect.isabstract(cls):
                    def parse_action(s, loc, tocs):
                        return cls(*tocs)
                    parser.setParseAction(parse_action)

    for var_name, value in locals().copy().items():
        if isinstance(value, pp.ParserElement):
            set_parse_action_magic(var_name, value)

    return start


parser = _make_parser()


def parse(prog: str)->StmtListNode:
    return parser.parseString(str(prog))[0]
