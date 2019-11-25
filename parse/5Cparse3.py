#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

_DCL    = Literal( 'DCL' )
_IDENT  = Literal( 'IDENT' )
_EQ     = Literal( '=' )
_CONST  = Literal( 'CONST' )
_RTN    = Literal( 'RETURN' )
_EOS    = Suppress( Literal( 'EOS' ) )
_PM     = oneOf( '+ -' )
_MD     = oneOf( '* /' )

_term   = Forward()
_factor = Forward()
_expr   = Optional( _PM ) + _term + ZeroOrMore( _PM + _term )

_term << _factor + ZeroOrMore( _MD + _factor )
_factor << ( _IDENT | _CONST | '(' + _expr + ')' )

_declare= _DCL + _IDENT + Optional( _EQ + (_CONST^_expr) )
#_declare= _DCL + _IDENT + Optional( _EQ + _CONST )
_return = _RTN + Optional( _CONST | _IDENT ) 
_assign = _IDENT + _EQ + _expr 
#_assign = _IDENT + _EQ + SkipTo( _EOS )

declare_stmt= _declare.setResultsName( 'DCL_STMT' )
return_stmt = _return.setResultsName ( 'RTN_STMT' )
assign_stmt = _assign.setResultsName ( 'ASN_STMT' )

statement=Forward()     # 再帰評価
statement<<  ( declare_stmt | return_stmt | assign_stmt )
#statement
 
st='''\
DCL IDENT
DCL IDENT = CONST
DLC IDENT = CONST * IDENT
RETURN
RETURN CONST
RETURN IDENT
IDENT = IDENT + IDENT
IDENT = IDENT * IDENT + CONST / CONST
IDENT = ( IDENT * IDENT ) + CONST / CONST
IDENT = - CONST + IDENT
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
