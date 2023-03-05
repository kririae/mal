#!/usr/bin/env python3

from mal_types import *
import printer


def mal_null(name: str) -> Callable[[Any], Any]:
    def func(*args, **kwargs) -> None:
        raise Exception(f"Symbol `{name}` not found")
    return func


def mal_type(args: List[MalExpression]) -> MalString:
    return MalString(str(type(args[0])))


def mal_exit(args: List[MalExpression]) -> None:
    raise EOFError()


def mal_plus(args: List[MalExpression]) -> MalInteger:
    return MalInteger(sum([i.naive() for i in args]))


def mal_minus(args: List[MalExpression]) -> MalInteger:
    return MalInteger(args[0].naive() - args[1].naive())


def mal_multiply(args: List[MalExpression]) -> MalInteger:
    return MalInteger(args[0].naive() * args[1].naive())


def mal_divide(args: List[MalExpression]) -> MalInteger:
    return MalInteger(args[0].naive() // args[1].naive())


def mal_prn(args: List[MalExpression]) -> MalNil:
    res = ' '.join(map(printer.pr_str, args))
    print(res)
    return MalNil()


def mal_pr_str(args: List[MalExpression]) -> MalString:
    return MalString(' '.join(map(printer.pr_str, args)))


def mal_str(args: List[MalExpression]) -> MalString:
    return MalString(''.join(map(lambda x: printer.pr_str(x, False), args)))


def mal_println(args: List[MalExpression]) -> MalString:
    res = ' '.join(map(lambda x: printer.pr_str(x, False), args))
    print(res)
    return MalNil()


def mal_list(args: List[MalExpression]) -> MalList:
    return MalList(args)


def mal_list_q(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(isinstance(args[0], MalList))


def mal_empty_q(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(len(args[0].naive()) == 0)


def mal_count(args: List[MalExpression]) -> MalInteger:
    if isinstance(args[0].naive(), list):
        return MalInteger(len(args[0].naive()))
    else:
        return 0


def mal_eq(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(args[0] == args[1])


def mal_lt(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(args[0] < args[1])


def mal_le(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(args[0] <= args[1])


def mal_gt(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(args[0] > args[1])


def mal_ge(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(args[0] >= args[1])


ns = {
    'nil':   MalNil(),
    'true':  MalBoolean(True),
    'false': MalBoolean(False),
    ###########################
    'prn':     MalHostFunction(mal_prn),
    'str':     MalHostFunction(mal_str),
    'pr-str':  MalHostFunction(mal_pr_str),
    'println': MalHostFunction(mal_println),
    'list':    MalHostFunction(mal_list),
    'list?':   MalHostFunction(mal_list_q),
    'empty?':  MalHostFunction(mal_empty_q),
    'count':   MalHostFunction(mal_count),
    ###########################
    '+':  MalHostFunction(mal_plus),
    '-':  MalHostFunction(mal_minus),
    '*':  MalHostFunction(mal_multiply),
    '/':  MalHostFunction(mal_divide),
    '=':  MalHostFunction(mal_eq),
    '<':  MalHostFunction(mal_lt),
    '<=': MalHostFunction(mal_le),
    '>':  MalHostFunction(mal_gt),
    '>=': MalHostFunction(mal_ge),
    ############################
    'type': MalHostFunction(mal_type),
    'exit': MalHostFunction(mal_exit),
}
