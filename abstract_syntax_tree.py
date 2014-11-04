"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

OPERATORS = {
    "=": lambda x, y: (x == y),
    "-": lambda x, y: x - y,
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y
}
PRECEDENCE = ["(", "|", "=", "-", "+", "*", "/"]
END = "\0"


def get_prec(operator):
    try:
        return PRECEDENCE.index(operator)
    except: pass
    if operator == END:
        return -1
    else:
        return len(PRECEDENCE)


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
                self.children[1].resolve()
            )


class SyntaxParser:
    def __init__(self, equation):
        self.equation = equation + END
        self.parsed = False

    def parse(self):
        self.index = 0
        self.tree = self.expect(get_prec(END) + 1)
        self.parsed = True

    def expect(self, prec):
        first = self.term()
        while get_prec(next(self)) >= prec:
            operator = next(self)
            self.consume()
            second = self.expect(get_prec(operator))
            first = Node(operator, first, second)
        return first

    def term(self):
        self.consume_ws()
        number = ""
        while next(self).isdigit():
            number += next(self)
            self.consume()
        self.consume_ws()
        return Node(int(number))

    def consume(self):
        self.index += 1

    def consume_ws(self):
        while next(self) == " ":
            self.index += 1

    def __next__(self):
        return self.equation[self.index]

    def get_tree(self):
        if self.parsed:
            return self.tree


def calc(eqn):
    s = SyntaxParser(eqn)
    s.parse()
    print(s.get_tree().resolve())
