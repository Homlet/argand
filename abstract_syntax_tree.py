"""Argand Diagram Plotter

abstract_syntax_tree.py - Produces an abstract syntax tree
                          from a mathematical expression
                          stored in a string.

Written by Sam Hubbard -  samlhub@gmail.com
"""

from collections import namedtuple
from math import factorial
import re
import inspect


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
    "^": "EXP"
}
OPERATORS = {
    "eqn": lambda x, y: x == y,
    "sub": lambda x, y: x - y,
    "add": lambda x, y: x + y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "exp": lambda x, y: x ** y,
    "mod": lambda x: abs(x),
    "neg": lambda x: -x,
}
GRAMMAR = {
    "eqn": ["sub rel sub"],
    "rel": ["MORE", "MEQL", "EQL", "LEQL", "LESS"],
    "sub": ["add SUB sub", "add"],
    "add": ["mul ADD add", "mul"],
    "mul": ["div MUL mul", "div"],
    "div": ["exp DIV div", "exp"],
    "exp": ["atm EXP exp", "atm"],
    "atm": ["NUM", "LPAR sub RPAR", "mod", "neg", "pos"],
    "mod": ["MOD sub MOD"],
    "neg": ["SUB atm"],
    "pos": ["ADD atm"]
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
            for i in range(len(regex_tokens)):
                regex_tokens[i] = "\\" + "\\".join(list(regex_tokens[i]))
            regex_tokens.append("[<>]?=")
            regex_tokens.append("[<>]")

            # Get list of tokens from regex.
            split = re.findall(
                "%s|[a-hj-z]|[\\d.]+|[\\d.]*i" % "|".join(regex_tokens),
                self.equation)
            print(split)
            tokens = [Token(TOKENS.get(x, "NUM"), x) for x in split]

            # Attempt to match the tokens to the grammar.
            match, remaining = self.match(self.root, tokens)
            if match and len(remaining) == 0:
                # Fix associativity issues caused by left recursion.
                match = self.fix_associativity(match)
                # Build and return the tree.
                return self.build(match)
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
        if match.rule == "NUM":
            # Create a leaf node containing the number.
            return Node(float(match.matched))

        # Create an alias for the child matches, and
        # force it to be a list.
        matched = match.matched
        if not isinstance(matched, list):
            matched = [matched]

        # Delete all child matches that just contain an
        # operator character, since they're useless now.
        i = 0
        while i < len(matched):
            if matched[i].rule not in self.ruleset \
            and matched[i].rule != "NUM":
                del matched[i]
            else:
                i += 1

        if match.rule in OPERATORS:
            # We have a rule node. We need to determine
            # if it is being used as a container or operator.
            # Then, we check if the number of child matches left is
            # the same as the expected number of arguments for the func.
            args = inspect.getargspec(OPERATORS[match.rule])[0]
            if len(matched) == len(args):
                # We have an operator node.
                return Node(
                    OPERATORS[match.rule],
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
