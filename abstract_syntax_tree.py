"""Argand Diagram Plotter

abstract_syntax_tree.py - Produces an abstract syntax tree
                          from a mathematical expression
                          stored in a string.

Written by Sam Hubbard -  samlhub@gmail.com
"""

from collections import namedtuple
import re


TOKENS = {
    "(": "LPAR",
    ")": "RPAR",
    "|": "MOD",
    "=": "EQL",
    "-": "SUB",
    "+": "ADD",
    "*": "MUL",
    "/": "DIV"
}
GRAMMAR = {
    "add": ["mul ADD add", "mul"],
    "mul": ["atm MUL mul", "atm"],
    "atm": ["NUM", "LPAR add RPAR", "MOD add MOD", "neg"],
    "neg": ["ADD atm"]
}
Token = namedtuple("Token", ["name", "value"])
Match = namedtuple("Match", ["rule", "matched"])


class Node:
    def __init__(self, value, *children):
        self.value = value
        self.children = children
        self.leaf = (len(children) == 0)

    def resolve(self):
        if isinstance(self.value, int):
            return self.value
        else:
            return OPERATORS[self.value](
                self.children[0].resolve(),
                self.children[1].resolve())

    def __repr__(self):
        s = str(self.value)
        s += "> "
        for child in self.children:
            s += str(child) + " "
        s += "<"
        return s


class SyntaxParser:
    def __init__(self, equation, ruleset=GRAMMAR):
        self.ruleset = ruleset
        split = re.findall(
            "[a-hj-z]|[\d.]+|[\d.]*i|[%s]" % "\\".join(TOKENS),
            equation)
        self.tokens = [Token(TOKENS.get(x, "NUM"), x) for x in split]
        print(self.match("add", self.tokens))

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
        return None, None
