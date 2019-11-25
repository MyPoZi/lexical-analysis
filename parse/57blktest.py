#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

declare   = Literal( 'DECLARE' )
ident     = Literal( 'IDENT'   )
const     = Literal( 'CONST'   )
opAssign  = Literal( '=' )
lparen    = Literal( '(' )
rparen    = Literal( ')' )
comma     = Literal( ',' )
lbrace    = Literal( '{' ).setResultsName( 'BGN' )
rbrace    = Literal( '}' ).setResultsName( 'END' )

opArith   = oneOf( '+ - * / ** %' )
opLogic   = oneOf( '== != <= < >= > && || !')
opBits    = oneOf( ' & | ^ ~ << >>' )
operator  = opArith ^ opLogic ^ opBits

factor    = ( Optional(lparen) + Optional( operator ) + Optional(lparen) +
                 ( ident ^ const ) + Optional( rparen ) )
term      = factor + ZeroOrMore( operator + factor )
expr      = term + ZeroOrMore( operator + term )

rsvReturn = Literal( 'return' )
rsvWhile  = Literal( 'while'  )
rsvIf     = Literal( 'if'     )
rsvElif   = Literal( 'elif'   )
rsvElse   = Literal( 'else'  )


_assign = ident + opAssign + expr
assignS = _assign.setResultsName( 'ASN' )

_declare = declare + (ident ^ _assign )
declareS = _declare.setResultsName('DCL')

_return  = rsvReturn + Optional( expr )
returnS  = _return.setResultsName( 'RTN' )

_while   = rsvWhile + expr
whileS   = _while.setResultsName( 'WHILE' )

ifS      = (rsvIf   + expr).setResultsName( 'IF'   )
elifS    = (rsvElif + expr).setResultsName( 'ELIF' )
elseS    = (rsvElse       ).setResultsName( 'ELSE' )
ifelS = ifS ^ elifS ^ elseS

elem = (ident|const) ^ _assign ^ _declare
_dclfunc = ( declare + ident + lparen +
             ZeroOrMore( elem + Optional( comma ) )  +
             rparen )
dclfuncS = _dclfunc.setResultsName( 'FNC' )

blockS = lbrace | rbrace

statement= declareS ^ assignS ^ returnS ^ whileS ^ ifelS ^ dclfuncS ^ blockS
#statement
 
st='''\
while (IDENT<CONST){
   IDENT=CONST
   IDENT=IDENT
}
if(IDENT>CONST){
   IDENT = CONST
} elif(!IDENT){
   IDENT=CONST*CONST
}
else
  IDENT=CONST
DECLARE IDENT(IDENT,CONST){
  IDENT=IDENT+IDENT+IDENT
  }
'''

'''
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
while IDENT { IDENT=CONST }
while (IDENT<CONST){ IDENT=CONST }
while (!IDENT&&CONST){ IDENT=CONST }
while !(IDENT&&CONST){ IDENT=CONST }
if(IDENT>CONST){ IDENT = CONST }
elif(!IDENT){ IDENT=CONST*CONST}
else IDENT=CONST
DECLARE IDENT(){ IDENT=CONST }
DECLARE IDENT(IDENT){ IDENT=IDENT*CONST }
DECLARE IDENT(IDENT,CONST){ IDENT=IDENT+IDENT+IDENT }
DECLARE IDENT(DECLARE IDENT, DECLARE IDENT)
DECLARE IDENT(DECLARE IDENT, DECLARE IDENT, DECLARE IDENT)

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
