#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
fi = 'tokenize0.pcl'

def main():
    l = pickle.load( open(fi, 'rb') )
    print(len(l))
    s =' '.join(
       [x['toktyp'] for x in l if x['toktyp']!='comment']  )
    r = [ ('EOS', 'EOS\n'), ('lbrace', 'lbrace\n'), \
          ('rbrace', 'rbrace\n'), ('\n ', '\n') ]
    s = rep(s, r)
    print(s)

def rep(s, r):
    t=s
    for i in r: t=t.replace(i[0], i[1] )
    return t

if __name__=='__main__': main() 

