#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

_DCL = Literal('DCL')
_IDENT = Literal('IDENT')
_EQ = Literal('=')
_CONST = Literal('CONST')
_RTN = Literal('RETURN')
_EOS = Suppress(Literal('EOS'))
_PM = oneOf('+ -')
_MD = oneOf('* /')
_WHL = Literal('WHILE')
lparen    = Literal( '(' )
rparen    = Literal( ')' )
lbrace = Literal('{')
rbrace = Literal('}')

_opLogic = oneOf('== != < <= > >= && ||')

_term = Forward()
_factor = Forward()
statement = Forward()  # 再帰評価

_expr = Optional(_PM) + _term + ZeroOrMore(_PM + _term)

_term << _factor + ZeroOrMore(_MD + _factor)
_factor << (_IDENT | _CONST | '(' + _expr + ')')

# _declare= _DCL + _IDENT + Optional( _EQ + _CONST )
# _assign = _IDENT + _EQ + SkipTo( _EOS )

_cond = (_expr + ZeroOrMore(_opLogic + _expr))
_declare = _DCL + _IDENT + Optional(_EQ + (_CONST ^ _expr))
_return = _RTN + Optional(_CONST | _IDENT)
_assign = _IDENT + _EQ + _expr
# _while  = _WHL + '(' +  _cond + ')'+ '{' + SkipTo( '}' )
_while = _WHL + lparen + _cond + rparen + lbrace + ZeroOrMore(statement) + rbrace

declare_stmt = _declare.setResultsName('DCL_STMT')
return_stmt = _return.setResultsName('RTN_STMT')
assign_stmt = _assign.setResultsName('ASN_STMT')
while_stmt = _while.setResultsName('WHL_STMT')

statement << (while_stmt ^ declare_stmt ^ return_stmt ^ assign_stmt)

st = '''\
WHILE ( CONST < IDENT ) {  }
WHILE ( CONST < IDENT ) { IDENT=CONST+IDENT }
WHILE ( CONST < IDENT ) { IDENT=IDENT EOS IDENT=CONST+IDENT EOS  }
WHILE ( CONST < IDENT ) { DCL IDENT EOS IDENT=CONST+IDENT EOS }
'''

r = statement

print('line   col  stmttype     tokentype')
print('----- ----- ------------ ---------------------')
for i in r.scanString(st):
    #   print(i)
    print('%5d %5d %-12s %-s' % (
        lineno(i[1], st), col(i[1], st),
        [x for x in i[0].asDict()][0],
        ' '.join([x for x in i[0]])))
