#!/usr/bin/env python3
from mal_types import *
from typing import List, Any
import re
pattern = re.compile(
    r'''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)''')


class Reader:
    def __init__(self, list_: List[Any]) -> None:
        self.pos_ = 0
        self.list_ = list_

    def __str__(self):
        return str(self.list_)

    def next(self) -> Any:
        ret = self.peek()
        self.pos_ += 1
        return ret

    def peek(self) -> Any:
        return self.list_[self.pos_]


def tokenize(s: str) -> List[str]:
    return pattern.findall(s)


def read_str(s: str):
    reader = Reader(tokenize(s.strip()))
    return read_form(reader)


def read_form(reader: Reader) -> MalExpression:
    specials = {
        '\'': 'quote',
        '`': 'quasiquote',
        '~': 'unquote',
        '~@': 'splice-unquote',
        '@': 'deref'
    }

    try:
        s = reader.peek()
        if not s:
            return MalEOF()
        elif s.startswith(';'):
            _ = reader.next()
            return read_form(reader)
        elif s == '(':
            _ = reader.next()
            return read_list(reader)
        elif s == '[':
            _ = reader.next()
            return read_vector(reader)
        elif s == '{':
            _ = reader.next()
            return read_hashmap(reader)
        elif s in specials.keys():
            _ = reader.next()
            element = read_form(reader)
            return MalList([MalSymbol(specials[s]), element])
        else:
            return read_atom(reader)
    except Exception as e:
        # print(str(e))
        return MalEOF()


def read_list(reader: Reader) -> MalList:
    lst = MalList()
    while True:
        s = reader.peek()
        if s == ')':
            _ = reader.next()
            break
        e = read_form(reader)
        if isinstance(e, MalEOF):
            raise Exception("list bracket not closed")
        lst.append(e)
    return lst


def read_vector(reader: Reader) -> MalVector:
    vec = MalVector()
    while True:
        s = reader.peek()
        if s == ']':
            _ = reader.next()
            break
        e = read_form(reader)
        if isinstance(e, MalEOF):
            raise Exception("vector bracket not closed")
        vec.append(e)
    return vec


def read_hashmap(reader: Reader) -> MalHashmap:
    vec = MalHashmap()
    while True:
        s = reader.peek()
        if s == '}':
            _ = reader.next()
            break
        e = read_form(reader)
        if isinstance(e, MalEOF):
            raise Exception("hashmap bracket not closed")
        vec.append(e)
    return vec


def read_atom(reader: Reader) -> MalExpression:
    specials = {
        'nil': lambda _: MalNil(),
        'true': lambda _: MalBoolean(True),
        'false': lambda _: MalBoolean(False),
    }

    s = reader.next()
    if check_int(s):
        return MalInteger(int(s))
    elif s[0] == '\"':
        return string_parser(s)
    elif s[0] == ')':
        raise Exception("Unexpected bracket")
    elif s[0] == ':':
        return MalKeyword(s)
    elif specials.get(s) is not None:
        return specials[s](s)
    else:
        return MalSymbol(s)


def check_int(s: str) -> bool:
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def string_parser(s: str) -> MalString:
    if s[0] != '\"':
        raise Exception("Invalid string")
    if len(s) < 2 or s[-1] != s[0]:
        raise Exception("String bracket not closed")
    s = s[1:-1]  # clamp string
    s_, idx = [], 0

    # Must iteratively parse the sequence
    while idx < len(s):
        c = s[idx]
        if c == '\\':
            if idx + 1 >= len(s):
                raise Exception("Error parsing string")
            next_c = s[idx+1]
            s_.append('\n' if next_c == 'n' else next_c)
            idx += 2
        else:
            s_.append(c)
            idx += 1
    return MalString(''.join(s_))


if __name__ == '__main__':
    print(read_str(r'''
;; Some inefficient arithmetic computations for benchmarking.

;; Unfortunately not yet available in tests of steps 4 and 5.

;; Compute n(n+1)/2 with a non tail-recursive call.
(def! sumdown
  (fn* [n]                              ; non-negative number
    (if (= n 0)
      0
      (+ n (sumdown  (- n 1))))))'''))
