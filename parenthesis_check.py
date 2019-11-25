#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

st = '''\
{ { x ( y ) (( z) x) {x} {y} }'''


def main(st):
    stk = list()
    err = False
    print('input:', st)
    print('index  char   operation   stack')
    print('-' * 30)
    for i, char in enumerate(st, start=1):
        err, operation = check_parenthesis(stk, char)
        if err:
            break
        print('%-3d:     %-6s %-10s %-20s' % (i, char, operation, ''.join(stk)))
    if err:
        print('error')
        return
    if len(stk) == 0:
        print('len(stack) = 0  OK')
    else:
        print('NG')


# カッコのチェックして、pushとpopする関数
# 返り値: Bool err, String operation
def check_parenthesis(stk, token):
    if token in '([{':
        stk.append(token)
        return False, 'push'

    # ) の場合の対応チェック
    if token == ')':
        if len(stk) == 0: return True, 'err'
        if stk[-1] == '(':
            stk.pop(-1)
            return False, 'pop'
        else:
            return True, 'err'

    # ] の場合の対応チェック
    elif token == ']':
        if len(stk) == 0: return True, 'err'
        if stk[-1] == '[':
            stk.pop(-1)
            return False, 'pop'
        else:
            return True, 'err'

    # } の場合の対応チェック
    elif token == '}':
        if len(stk) == 0: return True, 'err'
        if stk[-1] == '{':
            stk.pop(-1)
            return False, 'pop'
        else:
            return True, 'err'
    return False, 'pass'


if __name__ == '__main__':
    if len(sys.argv) == 2:
        st = open(sys.argv[1], 'r').read()
    main(st)
