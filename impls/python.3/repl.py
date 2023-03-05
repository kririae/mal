#!/usr/bin/env python3
import reader
import printer
from env import *
from core import *
from engine import reduce

import os
import readline

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')
repl_path = os.path.dirname(os.path.realpath(__file__))


# trivial functions
def read_(p): return reader.read_str(p)
def print_(p): return printer.pr_str(p)
def rep_(p, env): return print_(eval_(read_(p), env))
def eval_(ast, env): return reduce(ast, env)


def main():
    # Initialize execution environment
    env = get_core_env()

    try:
        with open(f"{repl_path}/core.mal", "r") as f:
            lines = f.readlines()
            # Load core.mal
            for line in lines:
                _ = rep_(line, env)
    except:
        pass
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
