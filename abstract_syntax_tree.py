"""Argand Diagram Plotter

abstract_syntax_tree.py - Produces an abstract syntax tree
                          from a mathematical expression
                          stored in a string.

Written by Sam Hubbard -  samlhub@gmail.com
"""

from collections import namedtuple
from cmath import *
import re
import inspect
import traceback


TOKENS = {
    "(": "LPAR",
    ")": "RPAR",
    "|": "MOD",
    ">": "MORE",
    ">=": "MEQL",
    "=": "EQL",
    "<=": "LEQL",
    "<": "LESS",
    "-": "SUB",
    "+": "ADD",
    "*": "MUL",
    "/": "DIV",
    "^": "EXP",
    "sin": "SIN",
    "cos": "COS",
    "tan": "TAN",
    "sqrt": "SQRT"
}
CODE = {
    "MORE": lambda x, y: x.real > y.real,
    "MEQL": lambda x, y: x.real >= y.real,
    "EQL":  lambda x, y: x == y,
    "LEQL": lambda x, y: x.real <= y.real,
    "LESS": lambda x, y: x.real < y.real,
    "sub": lambda x, y: x - y,
    "add": lambda x, y: x + y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "exp": lambda x, y: x ** y,
    "mod": lambda x: abs(x),
    "neg": lambda x: -x,
    "SIN": lambda x: sin(x),
    "COS": lambda x: cos(x),
    "TAN": lambda x: tan(x),
    "SQRT": lambda x: sqrt(x)
}
FUNCTIONS = ["SIN", "COS", "TAN", "SQRT"]
GRAMMAR = {
    "eqn": ["sub rel sub"],
    "rel": ["MORE", "MEQL", "EQL", "LEQL", "LESS"],
    "sub": ["add SUB sub", "add"],
    "add": ["mul ADD add", "mul"],
    "mul": ["div MUL mul", "div"],
    "div": ["exp DIV div", "exp"],
    "exp": ["atm EXP exp", "atm"],
    "atm": ["NUM", "VAR", "LPAR sub RPAR", "mod", "neg", "pos", "fun"],
    "mod": ["MOD sub MOD"],
    "neg": ["SUB atm"],
    "pos": ["ADD atm"],
    "fun": [fun + " atm" for fun in FUNCTIONS]
}


Token = namedtuple("Token", ["name", "value"])
Match = namedtuple("Match", ["rule", "matched"])


class Node:
    def __init__(self, value, *children):
        self.value = value
        self.children = children
        self.leaf = (len(children) == 0)

    def resolve(self):
        if callable(self.value):
            return self.value(*[child.resolve() for child in self.children])
        else:
            return self.value

    def __repr__(self):
        s = "[" + str(self.value) + "]("
        for c in self.children:
            s += str(c)
        s += ")"
        return s


class SyntaxParser:
    def __init__(self, equation, root="eqn", ruleset=GRAMMAR):
        super(SyntaxParser, self).__init__()
        self.equation = equation
        self.ruleset = ruleset
        self.root = root
        self.tree = None
        self.parsed = False

    def get_tree(self):
        if not self.parsed:
            self.tree = self.parse()
        return self.tree

    def parse(self):
        try:
            # Alter the tokens to play nicely with regex.
            regex_tokens = list(TOKENS)
            for t in ["<", "<=", "=", ">=", ">"]: regex_tokens.remove(t)
            escape = re.compile(
                r"[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]", re.IGNORECASE)
            for i in range(len(regex_tokens)):
                regex_tokens[i] = escape.sub(r"\\\g<0>", regex_tokens[i])
            regex_tokens.append(r"[<>]?=")
            regex_tokens.append(r"[<>]")

            # Get list of tokens from regex.
            split = re.findall(
                r"%s|[a-hj-z]|[\d.]*j|[\d.]+" % r"|".join(regex_tokens),
                self.equation)
            tokens = [
                Token(TOKENS.get(x, "VAR" if x.isalpha() else "NUM"), x)
                for x in split]

            # Attempt to match the tokens to the grammar.
            match, remaining = self.match(self.root, tokens)
            if match and len(remaining) == 0:
                # Fix associativity issues caused by left recursion.
                match = self.fix_associativity(match)
                # Build and return the tree.
                return self.build(match)
            else:
                raise Exception("Tokens invalid for grammar.")
        except:
            pass
        finally:
            self.parsed = True

    def match(self, rule, tokens):
        if tokens and rule == tokens[0].name:
            return Match(*tokens[0]), tokens[1:]
        for case in self.ruleset.get(rule, ()):
            remaining = tokens
            chain = []
            for subrule in case.split():
                matched, remaining = self.match(subrule, remaining)
                if not matched: break
                chain.append(matched)
            else:
                return Match(rule, chain), remaining
        return None, []

    def fix_associativity(self, match, rules=["sub", "div"]):
        def flatten(match):
            matched = recurse(match, flatten)
            if match.rule in rules \
            and len(matched) == 3  \
            and match.rule == matched[-1].rule:
                matched[-1:] = matched[-1].matched
            return Match(match.rule, matched)

        def build_left(match):
            matched = recurse(match, build_left)
            if match.rule in rules:
                while len(matched) > 3:
                    matched[:3] = [Match(match.rule, matched[:3])]
            return Match(match.rule, matched)

        return build_left(flatten(match))

    def build(self, match):
        # Create an alias for the child matches, and
        # force it to be a list.
        matched = match.matched
        if not isinstance(matched, list):
            matched = [matched]

        if match.rule == "NUM":
            # Create a leaf node containing the number.
            return Node(complex(matched[0]))
        elif match.rule == "VAR":
            # Create a leaf node representing a variable.
            return Node(matched[0])

        # Delete all child matches that just contain an
        # operator character, since they're useless now.
        i = 0
        while i < len(matched):
            if matched[i].rule not in self.ruleset \
            and matched[i].rule not in FUNCTIONS + ["NUM"]:
                del matched[i]
            else:
                i += 1

        if match.rule in ["eqn", "fun"]:
            # We need a special case for relations (equations)
            # as we need to snoop further down the tree to find
            # which type of relation to use.
            # We need a special case for functions for the same
            # reason, but the implementation is slightly different.
            operator = None
            if match.rule == "eqn":
                # This is a relation node.
                for i in range(len(matched)):
                    if matched[i].rule == "rel":
                        # Find and use the correct relation.
                        operator = matched[i].matched[0].rule
                        del matched[i]
                        break
            elif match.rule == "fun":
                # This is a function node.
                for i in range(len(matched)):
                    if matched[i].rule in FUNCTIONS:
                        # Find and use the correct function.
                        operator = matched[i].rule
                        del matched[i]
                        break

            # If we found an operator deeper in the tree, try to
            # create a node for it.
            if operator:
                # We have a supported operator, but do we have
                # the right number of arguments?
                args = inspect.getargspec(CODE[operator])[0]
                if len(matched) == len(args):
                    # We have the correct number of arguments.
                    return Node(
                        CODE[operator],
                        *[self.build(child) for child in matched])
                else:
                    raise Exception("Incorrect number of arguments.")
            else:
                raise Exception("Operator not found where expected.")
        elif match.rule in CODE:
            # We have a general rule node. We need to determine
            # if it is being used as a container or operator.
            # Then, we check if the number of child matches left is
            # the same as the expected number of arguments for the func.
            args = inspect.getargspec(CODE[match.rule])[0]
            if len(matched) == len(args):
                # We have an operator node.
                return Node(
                    CODE[match.rule],
                    *[self.build(child) for child in matched])
            else:
                # We just have a container (like sub), so build its child.
                return self.build(matched[0])
        else:
            # We just have a container (like atm).
            return self.build(matched[0])


def recurse(match, func):
    if match.rule in GRAMMAR:
        return list(map(func, match.matched))
    else:
        return match.matched
