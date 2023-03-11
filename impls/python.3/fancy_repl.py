#!/usr/bin/env python3
import reader
import printer
from env import *
from core import *
from engine import eval

import os
import sys
from typing import List
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding import KeyBindings
from pygments.lexers import ClojureLexer


# Set up a Pygments lexer with the Lisp syntax style
lexer = PygmentsLexer(ClojureLexer)

# Create a prompt session with the configured lexer and style
histfile = os.path.join(os.path.expanduser("~"), ".mal_history")
history = FileHistory(histfile)
session = PromptSession(lexer=lexer, prompt_continuation='    ',
                        complete_while_typing=True, history=history,
                        auto_suggest=AutoSuggestFromHistory())

# Add keybindings
kb = KeyBindings()
@kb.add('up')
def _(event): event.current_buffer.backward_history()
@kb.add('down')
def _(event): event.current_buffer.forward_history()


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
    repl_path = Path(os.path.dirname(os.path.realpath(__file__)))
    try:
        with open(repl_path / Path('core.mal'), 'r') as f:
            _ = rep_('(do ' + f.read() + ')', env)
    except:
        pass

    # Main loop
    while True:
        try:
            input_text = session.prompt(
                'mal> ', multiline=False, vi_mode=True, enable_system_prompt=True)
            if not input_text.strip():
                continue
            result = rep_(input_text, env)
            print(result)
        except KeyboardInterrupt:
            # Receives ctrl+c
            continue
        except EOFError:
            # Receives ctrl+d
            break
        except Exception as e:
            # Receives all other exception
            print(f'Error: {e}')


if __name__ == '__main__':
    main()
