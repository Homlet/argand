"""Argand Diagram Plotter

abstract_syntax_tree.py - Produces an abstract syntax tree
                          from a mathematical expression
                          stored in a string.

Written by Sam Hubbard -  samlhub@gmail.com
"""

from collections import namedtuple
import re
import inspect


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
OPERATORS = {
    "eql": lambda x, y: x == y,
    "sub": lambda x, y: x - y,
    "add": lambda x, y: x + y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "mod": lambda x: abs(x),
    "neg": lambda x: -x
}
GRAMMAR = {
    "eqn": ["add EQL add"],
    "sub": ["add SUB sub", "add"],
    "add": ["mul ADD add", "mul"],
    "mul": ["div MUL mul", "div"],
    "div": ["atm DIV div", "atm"],
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
            return self.tree("sub", self.equation)

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
        else:
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
