#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

_DCL    = Literal( 'DCL' )
_IDENT  = Literal( 'IDENT' )
_EQ     = Literal( '=' )
_CONST  = Literal( 'CONST' )

_declare = _DCL + _IDENT + Optional( _EQ + _CONST )
declare_stmt = _declare.setResultsName('DCL_STMT')

_RTN    = Literal( 'RETURN' )
_return = _RTN + Optional( _CONST | _IDENT ) 
return_stmt = _return.setResultsName( 'RTN_STMT' )

statement=Forward()     # 再帰評価
statement<<  ( declare_stmt | return_stmt )
#statement
 
st='''\
DCL IDENT
DCL IDENT = CONSTANT
RETURN
RETURN CONST
RETURN IDENT
'''

r = statement

print('line   col  stmttype     tokentype')
print('----- ----- ------------ ---------------------')
for i in r.scanString(st):
 #   print(i)
    print('%5d %5d %-12s %-s'%(
            lineno(i[1], st), col(i[1], st),
            [x for x in i[0].asDict()][0], 
            ' '.join([x for x in i[0]]) ) )
