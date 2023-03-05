import reader
import printer
from env import *
from core import *

import more_itertools as it


def flatten(ast: MalExpression, env: Env) -> MalExpression:
    """
        Flatten the aggregate structure in Mal
        i.e. will not reduce the size of MalList, MalVector or MalHashmap
    """
    if isinstance(ast, MalSymbol):
        return env.get(ast)
    if isinstance(ast, MalList):
        return MalList([reduce(i, env) for i in ast.naive()])
    if isinstance(ast, MalVector):
        return MalVector([reduce(i, env) for i in ast.naive()])
    if isinstance(ast, MalHashmap):
        return MalHashmap([reduce(v, env) if idx % 2 == 1 else v for idx, v in enumerate(ast.naive())])
    return ast


def reduce(ast: MalExpression, env: Env) -> MalExpression:
    """
        Reduce any structure in Mal
        i.e. will reduce MalList into a single
    """
    if not isinstance(ast, MalList):
        return flatten(ast, env)

    # Now that ast is a reducible MalList
    if len(ast.naive()) == 0:
        return ast

    # switch ast[0]
    if str(ast[0]) == 'def!':
        if not isinstance(ast[1], MalSymbol):
            raise Exception(
                "def! should be used with MalSymbol as the first parameter")
        res = reduce(ast[2], env)
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
            new_env.set(k, reduce(v, new_env))
        return reduce(ast[2], new_env)  # TODO: TCO
    elif str(ast[0]) == 'do':
        # Perform calculation and return the last
        return flatten(MalList(ast.naive()[1:]), env).naive()[-1]
    elif str(ast[0]) == 'if':
        cond = reduce(ast[1], env)
        # False section
        if isinstance(cond, MalNil) or (isinstance(cond, MalBoolean) and not cond.naive()):
            # If it evaluates to false and there isn't the third parameter
            if len(ast.naive()) == 3:
                return MalNil()
            # Else, evaluate it
            return reduce(ast[3], env)  # TODO: TCO
        else:
            return reduce(ast[2], env)  # TODO: TCO
    elif str(ast[0]) == 'fn*':
        def func(
            exprs: Optional[List[MalExpression]]
        ) -> MalExpression:
            # Initialize a new environment with
            new_env = Env(outer=env, binds=ast[1].naive(), exprs=exprs)
            return reduce(ast[2], new_env)
        return MalHostFunction(func)
    else:
        eval_list = flatten(ast, env)
        head, tail = eval_list[0], eval_list[1:]
        return head.call(tail)  # TODO: TCO
