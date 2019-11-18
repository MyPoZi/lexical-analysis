#!/usr/bin/env python
# -:- coding: utf-8 -:-

import re

def main():
    ''' 正規表現テストreg 変数stの内容を変更、正規表現指定を変更 '''
    st='''\
924-8383 076-274-7173 3-1 Yatsukaho, Hakusan-City
'''
    reg=[ r'\d+', r'[A-Z][a-z]+']
    for i in reg:
        print('\n'+i)
        print('start end   matched')
        print('----- ----- ------------------')
        for j in re.finditer( i, st ):
            print( '%5d %5d %-s'%
			(j.start(), j.end(), j.group())  )

if __name__=='__main__': main() 

