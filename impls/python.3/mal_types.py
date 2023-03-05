#!/usr/bin/env python3
from typing import List, Callable, Any
from typing_extensions import Self
from inspect import signature


class MalExpression:
    def naive(self) -> Any: return None
    def __repr__(self) -> str: return self.__str__()

    def __eq__(self, other: Self) -> bool:
        return type(self) == type(other) and self.naive() == other.naive()


class MalNil(MalExpression):
    def __init__(self) -> None: pass
    def __str__(self) -> str: return 'nil'


class MalBoolean(MalExpression):
    def __init__(self, val: bool) -> None: self.val = val
    def __str__(self) -> str: return 'true' if self.val else 'false'
    def naive(self) -> bool: return self.val


class MalEOF(MalExpression, object):
    def __str__(self): return 'EOF'


class MalSymbol(MalExpression, str):
    def __str__(self): return super().__str__()
    def naive(self): return self.__str__()


class MalKeyword(MalExpression, str):
    def __str__(self): return super().__str__()
    def naive(self): return self.__str__()


class MalAtom(MalExpression, object):
    def __init__(self, val) -> None: self.val = val
    def __str__(self): return str(self.val)
    def naive(self) -> Any: return self.val


class MalInteger(MalAtom):
    def __lt__(self, other: Self) -> bool:
        return type(self) == type(other) and self.naive() < other.naive()

    def __le__(self, other: Self) -> bool:
        return type(self) == type(other) and self.naive() <= other.naive()

    def __gt__(self, other: Self) -> bool:
        return type(self) == type(other) and self.naive() > other.naive()

    def __ge__(self, other: Self) -> bool:
        return type(self) == type(other) and self.naive() >= other.naive()


class MalString(MalAtom):
    def __str__(self): return str(self.val)

    def __repr__(self):
        return '\"' + str(self.val) \
            .replace("\\", "\\\\") \
            .replace("\n", "\\n") \
            .replace('"', '\\"') + '\"'


def array_eq(a: List, b: List):
    if type(a.naive()) != type(b.naive()):
        return False
    if len(a) != len(b):
        return False
    for idx, v in enumerate(a):
        if v != b[idx]:
            return False
    return True


class MalList(MalExpression, list):
    def __str__(self) -> str:
        return '(' + ' '.join([str(i) for i in self]) + ')'

    def __repr__(self) -> str:
        return '(' + ' '.join([repr(i) for i in self]) + ')'

    def naive(self) -> Self: return list(self)

    def __eq__(self, other: Self) -> bool:
        return array_eq(self, other)


class MalVector(MalExpression, list):
    def __str__(self):
        return '[' + ' '.join([str(i) for i in self]) + ']'

    def __repr__(self) -> str:
        return '[' + ' '.join([repr(i) for i in self]) + ']'

    def naive(self) -> Self: return list(self)

    def __eq__(self, other: Self) -> bool:
        return array_eq(self, other)


class MalHashmap(MalExpression, list):
    def __str__(self):
        return '{' + ' '.join([str(i) for i in self]) + '}'

    def __repr__(self) -> str:
        return '{' + ' '.join([repr(i) for i in self]) + '}'

    def naive(self) -> Self: return list(self)

    def __eq__(self, other: Self) -> bool:
        return array_eq(self, other)


class MalHostFunction(MalExpression):
    def __init__(
        self,
        func: Callable[[List[MalExpression]], MalExpression]
    ) -> None:
        super().__init__()
        self.func_ = func

    def __str__(self) -> str:
        return f'MalHostFunction {signature(self.func_)}'

    def __repr__(self) -> str:
        return '#<function>'

    def naive(self) -> Any:
        return self.func_

    def call(self, args: List[MalExpression]) -> MalExpression:
        return self.func_(args)


if __name__ == '__main__':
    print(repr())
