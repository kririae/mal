#!/usr/bin/env python3
import readline
from reader import *
from printer import *

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')


def READ(p):
    return read_str(p)


def EVAL(p):
    return p


def PRINT(p):
    return pr_str(p)


def rep(p):
    p = READ(p)
    p = EVAL(p)
    p = PRINT(p)
    return p


def main():
    while True:
        try:
            p = input("user> ")
        except EOFError:
            break
        print(rep(p))


if __name__ == '__main__':
    main()
