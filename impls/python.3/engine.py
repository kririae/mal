import reader
import printer
from env import *

import more_itertools as it
from typing import Tuple


def quasiquote(ast: MalExpression, enable_unquote: bool = True) -> MalExpression:
    def start_with_symbol(ast: MalExpression, sname: str) -> bool:
        """Helper function that performs a series of checking"""
        lst = ast.naive()
        return isinstance(lst, list)  \
            and len(lst) != 0  \
            and isinstance(lst[0], MalSymbol)  \
            and lst[0].naive() == sname

    if isinstance(ast, MalList):
        if start_with_symbol(ast, 'unquote') and enable_unquote:
            # if exists.. I don't want to do checking again
            return ast.naive()[1]
        else:
            lst = MalList()  # populate the list
            # Iterate over each element elt of ast in reverse order
            for elt in ast.naive()[::-1]:
                if start_with_symbol(elt, 'splice-unquote'):
                    lst = MalList([MalSymbol('concat'), elt.naive()[1], lst])
                else:
                    lst = MalList([MalSymbol('cons'), quasiquote(elt), lst])
            return lst
    elif isinstance(ast, MalHashmap) or isinstance(ast, MalSymbol):
        return MalList([MalSymbol('quote'), ast])
    elif isinstance(ast, MalVector):
        return MalList([MalSymbol('vec'), quasiquote(MalList(ast.naive()), False)])
    else:
        return ast


def flatten(ast: MalExpression, env: Env) -> MalExpression:
    """
    Flatten the aggregate structure in Mal
    i.e. will not reduce the size of MalList, MalVector or MalHashmap
    """
    if isinstance(ast, MalSymbol):
        return env.get(ast)
    if isinstance(ast, MalList):
        return MalList([eval(i, env) for i in ast.naive()])
    if isinstance(ast, MalVector):
        return MalVector([eval(i, env) for i in ast.naive()])
    if isinstance(ast, MalHashmap):
        return MalHashmap([eval(v, env) if idx % 2 == 1 else v for idx, v in enumerate(ast.naive())])
    return ast


def eval(ast: MalExpression, env: Env) -> MalExpression:
    """
    Reduce any structure in Mal
    i.e. will reduce MalList into a single

    TCO works with these ideas:
        1. eval(list) yet serves as a functionality to reduce list.
        2. If the *specials* or regular functions does not requires
           stack-based operations, use loop to perform it.
    """
    while True:
        if not isinstance(ast, MalList):
            return flatten(ast, env)

        # Now that ast is a reducible MalList
        if len(ast.naive()) == 0:
            return ast

        # switch ast[0]
        if str(ast[0]) == 'def!':
            # Some error checking
            if not isinstance(ast[1], MalSymbol):
                raise Exception(
                    "def! should be used with MalSymbol as the first parameter")
            # env.set will return the expression
            return env.set(ast[1], eval(ast[2], env))
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
                    raise Exception("Values must be bind to a symbol.")
                new_env.set(k, eval(v, new_env))

            env = new_env
            ast = ast[2]  # TCO
        elif str(ast[0]) == 'do':
            # Perform calculation and return the last
            # TODO: TCO
            ast = flatten(MalList(ast.naive()[1:]), env).naive()[-1]
        elif str(ast[0]) == 'if':
            cond = eval(ast[1], env)
            # False section
            if isinstance(cond, MalNil) or (isinstance(cond, MalBoolean) and not cond.naive()):
                # If it evaluates to false and there isn't the third parameter
                if len(ast.naive()) == 3:
                    return MalNil()
                # Else, evaluate it
                ast = ast[3]  # TCO
            else:
                ast = ast[2]  # TCO
        elif str(ast[0]) == 'fn*':
            def func(
                exprs: Optional[List[MalExpression]]
            ) -> Tuple[MalExpression, Env]:
                # Initialize a new environment with
                new_env = Env(outer=env, binds=ast[1].naive(), exprs=exprs)
                return (ast[2], new_env)
            return MalFunction(func)
        elif str(ast[0]) == 'quote':
            # The execution is terminated
            return ast[1]
        elif str(ast[0]) == 'quasiquoteexpand':
            return quasiquote(ast[1])
        elif str(ast[0]) == 'quasiquote':
            ast = quasiquote(ast[1])
        # elif str(ast[0]) == 'defmacro!':
        else:
            eval_list = flatten(ast, env)
            head, tail = eval_list[0], eval_list[1:]
            if isinstance(head, MalFunction):
                # If the function requires evaluation
                ast, env = head.call(tail)  # TCO
            elif isinstance(head, MalHostFunction):
                # If it is host function, directly evaluate it
                return head.call(tail)
            else:
                raise Exception(
                    f"Executing an unexpected symbol {str(ast[0])}")
