#!/usr/bin/env python3
from typing import List, Callable, Any
from inspect import signature


class MalExpression:
    def naive(self) -> Any:
        return self


class MalEOF(MalExpression, object):
    def __str__(self):
        return 'EOF'


class MalSymbol(MalExpression, str):
    pass


class MalAtom(MalExpression, object):
    def __init__(self, val) -> None:
        self.val = val

    def __str__(self):
        return str(self.val)

    def naive(self) -> Any:
        return self.val


class MalInteger(MalAtom):
    pass


class MalString(MalAtom):
    def __str__(self):
        return '\"' + str(self.val) + '\"'


class MalList(MalExpression, list):
    def __str__(self):
        res = ' '.join([str(i) for i in self])
        return '(' + res + ')'


class MalVector(MalExpression, list):
    def __str__(self):
        res = ' '.join([str(i) for i in self])
        return '[' + res + ']'


class MalFunction(MalExpression):
    def __init__(
        self,
        func: Callable[[List[MalExpression]], MalExpression]
    ) -> None:
        super().__init__()
        self.func_ = func

    def __str__(self) -> str:
        return f'MalFunction {signature(self.func_)}'

    def naive(self) -> Any:
        return self.func_

    def call(self, args: List[MalExpression]) -> MalExpression:
        return self.func_(args)
