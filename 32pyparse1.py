#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import *	# pyparsing利用

s = '''\
abc a10 123 4.5
'''		# テスト用文字列

r = Word( nums )		# 抽出条件
for i in r.scanString(s):	# マッチング
   print(i)

