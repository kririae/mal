#!/usr/bin/env python3

from mal_types import *
import printer
import reader


def mal_null(name: str) -> Callable[[Any], Any]:
    def func(*args, **kwargs) -> None:
        raise Exception(f"Symbol {name} not found")
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

def mal_mod(args: List[MalExpression]) -> MalBoolean:
    return MalInteger(args[0] % args[1])


# Here's where magic happens
def mal_read_string(args: List[MalExpression]) -> MalExpression:
    if not isinstance(args[0], MalString):
        raise Exception("The first argument of read-string should be a string")
    return reader.read_str(args[0].naive())


def mal_slurp(args: List[MalExpression]) -> MalString:
    if not isinstance(args[0], MalString):
        raise Exception("The first argument of slurp should be a string")
    with open(args[0].naive()) as f:
        return MalString(f.read())


# atom functions
def mal_atom(args: List[MalExpression]) -> MalAtom:
    return MalAtom(args[0])


def mal_atom_q(args: List[MalExpression]) -> MalBoolean:
    return MalBoolean(isinstance(args[0], MalAtom))


def mal_deref(args: List[MalExpression]) -> MalExpression:
    if not isinstance(args[0], MalAtom):
        raise Exception("The first argument of deref should be an atom")
    return args[0].naive()  # naive points to the value


def mal_reset(args: List[MalExpression]) -> MalExpression:
    if not isinstance(args[0], MalAtom):
        raise Exception("The first argument of reset should be an atom")
    args[0].val = args[1]
    return args[1]


def mal_cons(args: List[MalExpression]) -> MalList:
    if not isinstance(args[1].naive(), list):
        raise Exception("The second argument of cons should be a list")
    head, tail = args[0], args[1]
    return MalList([head] + args[1].naive())


def mal_concat(args: List[MalExpression]) -> MalList:
    return MalList([item for sublist in args for item in sublist.naive()])


def mal_vec(args: List[MalExpression]) -> MalList:
    return MalVector(args[0].naive())


def mal_nth(args: List[MalExpression]) -> MalExpression:
    assert isinstance(args[0].naive(), list)
    return args[0].naive()[args[1].naive()]


def mal_first(args: List[MalExpression]) -> MalExpression:
    if (not isinstance(args[0].naive(), list)) or len(args[0].naive()) == 0:
        return MalNil()
    return args[0].naive()[0]


def mal_rest(args: List[MalExpression]) -> MalExpression:
    if (not isinstance(args[0].naive(), list)):
        return MalList()
    return MalList(args[0].naive()[1:])


ns = {
    ###########################
    'prn':     MalHostFunction(mal_prn),
    'str':     MalHostFunction(mal_str),
    'pr-str':  MalHostFunction(mal_pr_str),
    'println': MalHostFunction(mal_println),
    'list':    MalHostFunction(mal_list),
    'list?':   MalHostFunction(mal_list_q),
    'empty?':  MalHostFunction(mal_empty_q),
    'count':   MalHostFunction(mal_count),

    'read-string': MalHostFunction(mal_read_string),
    'slurp':       MalHostFunction(mal_slurp),
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
    '%':  MalHostFunction(mal_mod),
    ############################
    'atom':   MalHostFunction(mal_atom),
    'atom?':  MalHostFunction(mal_atom_q),
    'deref':  MalHostFunction(mal_deref),
    'reset!': MalHostFunction(mal_reset),
    # 'swap!': ...
    ############################
    # List manipulation
    'cons':   MalHostFunction(mal_cons),
    'concat': MalHostFunction(mal_concat),
    'vec':    MalHostFunction(mal_vec),
    'nth':    MalHostFunction(mal_nth),
    'first':  MalHostFunction(mal_first),
    'rest':   MalHostFunction(mal_rest),
    ############################
    'type': MalHostFunction(mal_type),
    'exit': MalHostFunction(mal_exit),
}
