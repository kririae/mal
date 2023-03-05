#!/usr/bin/env python3
from mal_types import *
from reader import *


def pr_str(t: MalExpression) -> str:
    return str(t).strip()


if __name__ == '__main__':
    t = read_str('( )')
    print(pr_str(t))
