#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, pickle
from pyparsing import *

st = '''\
// example1
float main(){
   int a1=10;
   float bif;
   bif=a1*2/10.5-1.4e-5;
   if a1>20 { bif=a; } else { bif=1.5; }
   print("ans=", bif);
   return(bif);
}
'''
# pyparsing rule definition
comment  = cppStyleComment.setResultsName( 'comment' )

string   = quotedString.setResultsName( 'string' )
integer  = Word( nums ).setResultsName( 'integer' )
real     = Combine( integer+'.'+integer ).setResultsName( 'real')
exppart  = oneOf('e E')+Optional( oneOf('+ -') )+integer
realexp  = Combine( (real|integer)+exppart ).setResultsName( 'realexp')
constant = string | realexp | real | integer

ident    = Word( alphas, alphanums ).setResultsName( 'identifier' )
declare  = oneOf( 'int float boolean void').setResultsName( 'declare' )
reserved = oneOf( 'if else while return').setResultsName( 'reserved' )

opeArith = oneOf( '+ - * / % ** =' ).setResultsName( 'opeArith' )
opeLogic = oneOf( '== != < <= >= > && || !' ).setResultsName( 'opeLogic' )
opeBits  = oneOf( '& | ^ ~' ).setResultsName( 'opeBits' )
operator = opeLogic | opeLogic | opeArith

lparen   = Literal( '(' ).setResultsName( 'lparen' )
rparen   = Literal( ')' ).setResultsName( 'rparen' )
lbrace   = Literal( '{' ).setResultsName( 'lbrace' )
rbrace   = Literal( '}' ).setResultsName( 'rbrace' )
eos      = Literal( ';' ).setResultsName( 'EOS' )
comma    = Literal( ',' ).setResultsName( 'comma' )
punction = lparen | rparen | lbrace | rbrace | eos | comma
# parse rule
r = comment | reserved | declare | constant | ident | operator | punction

def main(st):
    l=list()
    print('line  col   len   type            token')
    print('----- ----- ----- --------------- '+'-'*20)
    for i in r.scanString( st ):
#        print(i)       # 結果がおかしければこのコメントをとって確認
        li = lineno(i[1], st)       # 行番号を得る
        co = col(i[1], st)          # 桁位置を得る
        le = i[2]-i[1]              # トークン長さ
        to = i[0][0]                # トークン文字列
        ty = [x for x in i[0].asDict()][0] # トークンタイプを得る
        if type(to)!=type(str()): to=to[0] # 複数の条件となっている場合
        print('%5d %5d %5d %-10s %-20s'%(li, co, le, ty, to) )
        l.append(
            dict(token=to, toktyp=ty, line=li, col=co, len=le)
        )
    print('EOF')
    print('%d token detected'%len(l))
    # printToken(l)
    pprint(l)
    pickle.dump( l, open('tokenize0.pcl', 'wb') )

def printToken(l):
    print( ' '.join([x['token'] for x in l] ) )

def pprint(l1):
    ''' pretty print '''
    l=l1    # 引数を変更するのでコピー
    print('\npretty print')
    for i in l:
        if i['toktyp']=='comment': i['token']+='\n'   # 改行付与
    s = ' '.join( [x['token'] for x in l] ) # 半角スペースで連結
    r = [ ('{','\n{\n'), ('}','\n}\n'), (';',';\n'),
           ('\n ','\n'),('\n\n', '\n') ]
    s = rep(s, r)           # 文字列置換
    no, lev = 1, 0          # 行番号，ブロックレベル
    sp = '%5d %2d '%(no, lev); no+=1 # 最初の行番号
    for i in range(len(s)): # 1文字ずつ確認
        if s[i]=='{': lev+=1                    # ブロック開始
        if i<len(s)-1 and s[i+1]=='}': lev-=1   # ブロック終了
        sp+=s[i]
        if s[i]=='\n':
            sp+='%5d %2d '%(no,lev)+' '*4*lev     # 行番号と字下げ
            no+=1
    print(sp)

def rep(s, r):
    t=s         # 引数を変更するのでコピー
    for i in r:
        t=t.replace(i[0], i[1])
    return t

if __name__=='__main__':
    if len(sys.argv)==2:
        st=open(sys.argv[1], 'r').read()
    main(st)


