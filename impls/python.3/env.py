#!/usr/bin/env python3
from mal_types import *
from core import *

from typing import Any, Optional
from typing_extensions import Self


class Env:
    def __init__(
        self,
        outer: Optional[Self] = None,
        binds: Optional[List[MalExpression]] = None,
        exprs: Optional[List[MalExpression]] = None
    ) -> None:
        # Initialize base env
        self.outer = outer
        self.data = {}
        if binds is not None and exprs is not None:
            for idx, s in enumerate(binds):
                if s.naive() == '&':
                    self.set(binds[idx+1], MalList(exprs[idx:]))
                    break
                self.set(s, exprs[idx])

    def set(self, s: MalSymbol, v: MalExpression):
        """takes a symbol key and a mal value and adds to the data structure"""
        if not isinstance(s, MalSymbol):
            raise Exception(
                "Unmatched data type encountered in environment")
        self.data[str(s)] = v

    def find(self, s: MalSymbol) -> Self:
        """Find a match environment with MalSymbol

        takes a symbol key and if the current environment contains that key then return the environment. If no key is found and outer is not nil then call find (recurse) on the outer environment.
        """
        s = str(s)
        if self.data.get(s) is not None:
            return self
        elif self.outer is None:
            return get_core_env()
        else:
            return self.outer.find(s)

    def get(self, s: MalSymbol) -> MalExpression:
        """Find the match expr with MalSymbol

        takes a symbol key and uses the find method to locate the environment with the key, then returns the matching value. If no key is found up the outer chain, then throws/raises a "not found" error.
        """
        s = str(s)
        env = self.find(s)
        return env.data.get(s, MalHostFunction(mal_null(name=s)))


def get_core_env() -> Env:
    base = Env()
    # Load core.py
    for k, v in ns.items():
        base.set(MalSymbol(k), v)
    return base


if __name__ == '__main__':
    pass
