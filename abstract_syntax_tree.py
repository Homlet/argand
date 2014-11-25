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
    "-": "ADD",
    "+": "ADD",
    "*": "MUL",
    "/": "MUL"
}
OPERATORS = {
    "-": lambda x, y: x - y,
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "=": lambda x, y: x == y
}
GRAMMAR = {
    "eqn": ["add EQL add"],
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
        if len(self.children) == 2:
            return self.value(
                self.children[0].resolve(),
                self.children[1].resolve())
        else:
            return self.value

    def __repr__(self):
        s = "[" + str(self.value) + "]("
        for c in self.children:
            s += " " + str(c)
        s += ")"
        return s


class SyntaxParser:
    def __init__(self, equation, ruleset=GRAMMAR):
        self.equation = equation
        self.ruleset = ruleset

    def get_tree(self):
        eqn = self.tree("eqn", self.equation)
        if eqn:
            return eqn
        else:
            return self.tree("add", self, equation)

    def tree(self, rule, equation):
        split = re.findall(
            "[a-hj-z]|[\d.]+|[\d.]*i|[%s]" % "\\".join(TOKENS),
            equation)
        tokens = [Token(TOKENS.get(x, "NUM"), x) for x in split]
        match = self.match(rule, tokens)[0]
        if match:
            match = self.fix_associativity(match)
            return self.build(match)
        else:
            return None

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

    def fix_associativity(self, match, rules=["add", "mul"]):
        def flatten(match):
            matched = recurse(match, flatten)
            if match.rule in rules \
            and len(matched) == 3           \
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
        matched = match.matched
        if not isinstance(matched, list):
            matched = [matched]
        if len(matched) == 1:
            if match.rule in self.ruleset:
                return self.build(matched[0])
            else:
                return Node(float(matched[0]))
        else:
            return Node(
                OPERATORS[matched[1].matched],
                self.build(matched[0]),
                self.build(matched[2]))


def recurse(match, func):
    if match.rule in GRAMMAR:
        return list(map(func, match.matched))
    else:
        return match.matched
