#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

declare   = Literal( 'DECLARE' )
ident     = Literal( 'IDENT'   )
const     = Literal( 'CONST'   )
opAssign  = Literal( '='       )
lparen    = Literal( '(' )
rparen    = Literal( ')' )

opArith   = oneOf( '+ - * / ** %' )
opLogic   = oneOf( '== != <= < >= > && || !')
opBits    = oneOf( ' & | ^ ~ << >>' )
operator  = opArith ^ opLogic ^ opBits

factor = Optional(lparen)+Optional( operator ) + ( ident ^ const )+Optional(rparen)
term   = factor + ZeroOrMore( operator + factor )
expr   = term + ZeroOrMore( operator + term )

rsvReturn = Literal( 'return' )

_assign = ident + opAssign + expr
assignS = _assign.setResultsName( 'ASN' )

#_declare = declare + ident + Optional( opAssign + ( const ^ expr )  )
_declare = declare + (ident ^ _assign )
declareS = _declare.setResultsName('DCL')

_return  = rsvReturn + Optional( expr )
returnS  = _return.setResultsName( 'RTN' )

statement= declareS ^ assignS ^ returnS
#statement
 
st='''\
DECLARE IDENT
DECLARE IDENT = CONST
DECLARE IDENT = CONST * IDENT 
IDENT=-CONST
IDENT=IDENT+CONST
IDENT=IDENT*IDENT+CONST/CONST
IDENT=(IDENT+IDENT)
IDENT=IDENT*(IDENT+IDENT)
return
return IDENT
return IDENT+IDENT
return (IDENT*IDENT+CONST)
'''

r = statement

print('line   col  stmt   DSL')
print('----- ----- ------ ---------------------')
for i in r.scanString(st):
#    print(i)
    ty=[x for x in i[0].asDict().keys()  ]
    if 'WHILE_STMT' in ty: ty='WHILE_STMT'
    else: ty=ty[0] 
    print('%5d %5d %-6s %-s'%(
            lineno(i[1], st), col(i[1], st),
            ty,
            ' '.join([x for x in i[0]]) ) )
