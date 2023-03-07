#!/usr/bin/env python3
import reader
import printer
from env import *
from core import *
from engine import eval

import os
import sys
import atexit
import readline
from pathlib import Path

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')
repl_path = Path(os.path.dirname(os.path.realpath(__file__)))
histfile = os.path.join(os.path.expanduser("~"), ".mal_history")
try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


def read_(p): return reader.read_str(p)
def print_(p): return printer.pr_str(p)
def rep_(p, env): return print_(eval_(read_(p), env))
def eval_(ast, env): return eval(ast, env)


def mal_swap(args: List[MalExpression]) -> MalExpression:
    if not isinstance(args[0], MalAtom):
        raise Exception("The first argument of reset should be an atom")
    atom, func = args[0], args[1]
    if isinstance(func, MalHostFunction):
        atom.val = func.call([atom.val] + args[2:])
    elif isinstance(func, MalFunction):
        ast, env = func.call([atom.val] + args[2:])
        atom.val = eval(ast, env)
    else:
        raise Exception("Unexpected argument")
    return atom.val


def main():
    # Initialize execution environment
    env = get_core_env()
    _ = env.set(MalSymbol('eval'), MalHostFunction(
        lambda args: eval_(args[0], env)))
    _ = env.set(MalSymbol('swap!'), MalHostFunction(mal_swap))
    _ = env.set(MalSymbol('*ARGV*'),
                MalList([MalString(str(i)) for i in sys.argv[2:]]))

    # Load core.mal
    try:
        with open(repl_path / Path('core.mal'), 'r') as f:
            _ = rep_('(do ' + f.read() + ')', env)
    except:
        pass

    if len(sys.argv) > 1:
        rep_(f'(load-file "{sys.argv[1]}")', env)
        return

    # Main loop
    while True:
        try:
            p = input("user> ")
            readline.add_history(p)
            print(rep_(p, env))
        except EOFError:
            # Receives ctrl+d
            break
        except Exception as e:
            # Receives all other exception
            print(str(e))


if __name__ == '__main__':
    main()
