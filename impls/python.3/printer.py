#!/usr/bin/env python3
from mal_types import *
from reader import *


def pr_str(
    t: MalExpression,
    print_readably: bool = True
) -> str:
    return repr(t) if print_readably else str(t)


if __name__ == '__main__':
    t = read_str('( )')
    print(pr_str(t))
