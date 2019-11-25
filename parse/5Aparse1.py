#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *

_DCL = Literal('DCL')
_IDENT = Literal('IDENT')
_EQ = Literal('=')
_CONST = Literal('CONST')
_RTN = Literal('RETURN')
_EOS = Suppress(Literal('EOS'))

_declare = _DCL + _IDENT + Optional(_EQ + _CONST)
_return = _RTN + Optional(_CONST | _IDENT)
_assign = _IDENT + _EQ + SkipTo(_EOS)

declare_stmt = _declare.setResultsName('DCL_STMT')
return_stmt = _return.setResultsName('RTN_STMT')
assign_stmt = _assign.setResultsName('ASN_STMT')

statement = Forward()  # 再帰評価
statement << (declare_stmt | return_stmt | assign_stmt)
# statement

# DECLARE 宣言 int、float
# IDENT 識別子 変数名、関数名、クラス名
# CONST 定数 数値、文字列
# int a = 1 -> DECLARE IDENT = CONST -> _DCL + _IDENT + Optional(_EQ + _CONST) -> DCL_STMT


st = '''\
DCL IDENT
DCL IDENT = CONST
RETURN
RETURN CONST
RETURN IDENT
IDENT = IDENT + IDENT EOS
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
