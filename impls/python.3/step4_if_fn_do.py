#!/usr/bin/env python3
import readline
import more_itertools as it

import reader
import printer
from env import *

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')


def flatten(ast: MalExpression, env: Env) -> MalExpression:
    """
        Flatten the aggregate structure in Mal
        i.e. will not reduce the size of MalList or MalVector
    """
    if isinstance(ast, MalSymbol):
        return env.get(ast)
    if isinstance(ast, MalList):
        return MalList([EVAL(i, env) for i in ast])
    if isinstance(ast, MalVector):
        return MalVector([EVAL(i, env) for i in ast])
    return ast


def READ(p):
    return reader.read_str(p)


def EVAL(ast: MalExpression, env: Env) -> MalExpression:
    """
        Reduce any structure in Mal
        i.e. will reduce MalList into a single
    """
    if not isinstance(ast, MalList):
        return flatten(ast, env)

    # Now that ast is a reducible MalList
    if len(ast.naive()) == 0:
        return ast
    if str(ast[0]) == 'def!':
        if not isinstance(ast[1], MalSymbol):
            raise Exception(
                "def! should be used with MalSymbol as the first parameter")
        res = EVAL(ast[2], env)
        env.set(ast[1], res)
        return res
    elif str(ast[0]) == 'let*':
        if not (isinstance(ast[1], MalList) or
                isinstance(ast[1], MalVector)):
            raise Exception(
                "let* should be used with a MalList or MalVector as bindings")
        if len(ast[1].naive()) % 2 != 0:
            raise Exception("Invalid binding list")
        # Create a new environment chained below
        new_env = Env(outer=env)
        binding_list = it.batched(ast[1].naive(), 2)
        for k, v in binding_list:
            if not isinstance(k, MalSymbol):
                raise Exception("Values must be bind to an symbol.")
            new_env.set(k, EVAL(v, new_env))
        return EVAL(ast[2], new_env)
    else:
        eval_list = flatten(ast, env)
        head, tail = eval_list[0], eval_list[1:]
        return head.call(tail)


def PRINT(p):
    return printer.pr_str(p)


def rep(p, env):
    p = READ(p)
    p = EVAL(p, env)
    p = PRINT(p)
    return p


def main():
    # Initialize execution environment
    env = get_base_env()
    while True:
        try:
            p = input("user> ")
            readline.add_history(p)
            print(rep(p, env))
        except EOFError:
            # Receives ctrl+d
            break
        except Exception as e:
            # Receives all other exception
            print(str(e))


if __name__ == '__main__':
    main()
