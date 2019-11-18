#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyparsing import *

#ここに調べる文字列（cソース）を書く
st = '''\
1 20  /* comment */
'''

# トークン分割のルール
integer = Word( nums ).setResultsName( 'integer' )
comment = cppStyleComment.setResultsName( 'comment' )

# 条件を追加したらここにも追加する 追加する位置は動かして確認すること
r = (comment|integer)

def main(st):
    ''' トークン分割 '''
    print('line  col   len   type            token')
    print('----- ----- ----- '+'-'*10+' '+'-'*20)

    for i in r.scanString( st ):
#        print(i)			# 結果がおかしければ行頭のコメントをとって確認
        li = lineno(i[1], st)		# 行番号を得る
        co = col(i[1], st)			# 桁位置を得る
        le = i[2]-i[1]			# トークン長さ
        to = i[0][0]			# トークン文字列
        ty = [x for x in i[0].asDict()][0]	# トークンを得る
        if type(to)!=type(str()): to=to[0]	# 複数の条件となっている場合
        print('%5d %5d %5d %-10s %-20s'%(li, co, le, ty, to) )

if __name__=='__main__': main(st)

