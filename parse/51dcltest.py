#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

declare   = Literal( 'DECLARE' )
ident     = Literal( 'IDENT'   )
opAssign  = Literal( '='       )
const     = Literal( 'CONST'   )

                            
_declare = declare + ident + Optional( opAssign + ( const ^ ident )  )
declareS = _declare.setResultsName('DCL')

statement=   declareS 

# テストDSL 
st='''\
DECLARE IDENT
DECLARE IDENT = CONST
DECLARE IDENT = IDENT
'''

r = statement

print('line   col  stmt   DSL')
print('----- ----- ------ ---------------------')
for i in r.scanString(st):
#    print(i)
    ty=[x for x in i[0].asDict().keys()  ][0]
    print('%5d %5d %-6s %-s'%(
            lineno(i[1], st), col(i[1], st), ty,
            ' '.join([x for x in i[0]]) ) )
