#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

declare = Literal('DECLARE')
ident = Literal('IDENT')
const = Literal('CONST')
opAssign = Literal('=')
lparen = Literal('(')
rparen = Literal(')')

opArith = oneOf('+ - * / ** %')
opLogic = oneOf('== != <= < >= > && || !')
opBits = oneOf(' & | ^ ~ << >>')
operator = opArith ^ opLogic ^ opBits

factor = (Optional(lparen) + Optional(operator) + Optional(lparen) +
          (ident ^ const) + Optional(rparen))
term = factor + ZeroOrMore(operator + factor)
expr = term + ZeroOrMore(operator + term)

rsvReturn = Literal('return')
rsvWhile = Literal('while')
rsvIf = Literal('IF')
rsvElif = Literal('elif')
rsvElse = Literal('ELSE')

_assign = ident + opAssign + expr
assignS = _assign.setResultsName('ASN')

_declare = declare + (ident ^ _assign)
declareS = _declare.setResultsName('DCL')

_return = rsvReturn + Optional(expr)
returnS = _return.setResultsName('RTN')

_while = rsvWhile + expr
whileS = _while.setResultsName('while')

statement = Forward()

# なんでかIFを認識しない、parse4のWHILEも同様
# {}の中に式がなければ認識する
# _if = rsvIf + expr + '{' + ZeroOrMore(statement) + '}'

_if = rsvIf + expr + '{' + SkipTo('}')
_else = rsvElse + '{' + SkipTo('}')

ifS = _if.setResultsName('IF')
elifS = (rsvElif + expr).setResultsName('ELIF')
elseS = _else.setResultsName('ELSE')
ifelS = ifS ^ elifS ^ elseS

# statement = declareS ^ assignS ^ returnS ^ whileS ^ ifelS
statement << (declareS ^ assignS ^ returnS ^ whileS ^ ifelS)
# statement

st = '''\
IF CONST > CONST { IDENT = COST }
IF CONST == IDENT { IDENT = CONST EOS IDENT = IDENT EOS }
IF CONST != IDENT { IDENT = CONST } ELSE { IDENT = CONST + IDENT }
'''

r = statement

print('line   col  stmt   DSL')
print('----- ----- ------ ---------------------')
for i in r.scanString(st):
    #    print(i)
    ty = [x for x in i[0].asDict().keys()]
    if 'WHILE_STMT' in ty:
        ty = 'WHILE_STMT'
    else:
        ty = ty[0]
    print('%5d %5d %-6s %-s' % (
        lineno(i[1], st), col(i[1], st),
        ty,
        ' '.join([x for x in i[0]])))
