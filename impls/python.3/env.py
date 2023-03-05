#!/usr/bin/env python3
from mal_types import *
from typing import Any
from typing_extensions import Self


class Env:
    def __init__(self, outer: Self = None) -> None:
        # Initialize base env
        self.outer = outer
        self.data = {}

    def set(self, s: MalSymbol, v: MalExpression):
        """takes a symbol key and a mal value and adds to the data structure"""
        self.data[s] = v

    def find(self, s: MalSymbol) -> Self:
        """Find a match environment with MalSymbol

        takes a symbol key and if the current environment contains that key then return the environment. If no key is found and outer is not nil then call find (recurse) on the outer environment.
        """
        if self.data.get(s) is not None:
            return self
        elif self.outer is None:
            return get_base_env()
        else:
            return self.outer.find(s)

    def get(self, s: MalSymbol) -> MalExpression:
        """Find the match expr with MalSymbol

        takes a symbol key and uses the find method to locate the environment with the key, then returns the matching value. If no key is found up the outer chain, then throws/raises a "not found" error.
        """
        env = self.find(s)
        return env.data.get(s, MalFunction(mal_null(name=s)))


def mal_null(name: str) -> Callable[[Any], Any]:
    def func(*args, **kwargs) -> None:
        raise Exception(f"symbol {name} not found")
    return func


def mal_plus(args: List[MalExpression]) -> MalInteger:
    return MalInteger(sum([i.naive() for i in args]))


def mal_minus(args: List[MalExpression]) -> MalInteger:
    return MalInteger(args[0].naive() - args[1].naive())


def mal_multiply(args: List[MalExpression]) -> MalInteger:
    return MalInteger(args[0].naive() * args[1].naive())


def mal_divide(args: List[MalExpression]) -> MalInteger:
    return MalInteger(args[0].naive() // args[1].naive())


def get_base_env() -> Env:
    base = Env()
    data = {
        '+': MalFunction(mal_plus),
        '-': MalFunction(mal_minus),
        '*': MalFunction(mal_multiply),
        '/': MalFunction(mal_divide),
    }
    for k, v in data.items():
        base.set(MalSymbol(k), v)
    return base


if __name__ == '__main__':
    env = get_base_env()
    print(env.get('qwq'))
