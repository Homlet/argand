"""Abstract Syntax Tree

Contains classes for parsing and inspecting abstract syntax trees
involving letter variables, functions and complex numbers.

Written by Sam Hubbard -  samlhub@gmail.com
"""

import cmath
import inspect
import re
from collections import namedtuple


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
    "sqrt": "SQRT",
    "arg": "ARG"
}
CODE = {
    "MORE": lambda x, y: x.real > y.real,
    "MEQL": lambda x, y: x.real >= y.real,
    "EQL":  lambda x, y: x == y,
    "LEQL": lambda x, y: x.real <= y.real,
    "LESS": lambda x, y: x.real < y.real,
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "exp": lambda x, y: x ** y,
    "mod": lambda x: abs(x),
    "pos": lambda x: x,
    "neg": lambda x: -x,
    "SIN": lambda x: cmath.sin(x),
    "COS": lambda x: cmath.cos(x),
    "TAN": lambda x: cmath.tan(x),
    "SQRT": lambda x: cmath.sqrt(x),
    "ARG": lambda x: cmath.phase(x)
}
FUNCTIONS = ["SIN", "COS", "TAN", "SQRT", "ARG"]
GRAMMAR = {
    "eqn": ["add rel add"],
    "rel": ["MORE", "MEQL", "EQL", "LEQL", "LESS"],
    "add": ["sub ADD add", "sub"],
    "sub": ["mul SUB sub", "mul"],
    "mul": ["div MUL mul", "div"],
    "div": ["exp DIV div", "exp"],
    "exp": ["atm EXP exp", "atm"],
    "atm": ["NUM", "VAR", "par", "mod", "neg", "pos", "fun"],
    "par": ["LPAR add RPAR"],
    "mod": ["MOD add MOD"],
    "neg": ["SUB atm"],
    "pos": ["ADD atm"],
    "fun": [fun + " atm" for fun in FUNCTIONS]
}


Token = namedtuple("Token", ["name", "value"])
Match = namedtuple("Match", ["rule", "matched"])


NODE_TYPE_NUM = 0
NODE_TYPE_VAR = 1
NODE_TYPE_OP = 2


class Node:
    """A node used to build an AST.
    
    Can store a numerical value, or a function to apply to its child(ren).
    
    Attributes:
        type: Whether the node is numerical, a function or a variable.
        value: The value stored in the node.
        children: A list of child node objects.
        parent: A reference to the node's parent, if one exists.
    """

    def __init__(self, type, value, *children):
        """Create node with value and children.

        Args:
            type: See Node.type.
            value: See Node.value.
            children: See Node.children.
        """
        self.type = type
        self.value = value
        self.children = children
        self.parent = None
        for child in self.children:
            child.parent = self

    def resolve(self):
        """Recursively resolve the tree up to this node.
        
        Returns:
            If the node stores a numerical value, returns the node's value.
            Otherwise return the node's function applied to it's children.
        """
        if self.type == NODE_TYPE_OP:
            return self.value(*[child.resolve() for child in self.children])
        else:
            return self.value

    def __repr__(self):
        """Represent the node as a string.
        
        Used for debugging purposes.
        """
        s = "[" + str(self.value) + "]("
        for c in self.children:
            s += str(c)
        s += ")"
        return s


class SyntaxParser:
    """Parses an input string to an AST.

    Attributes:
        equation: The input string to parse.
        ruleset: A set of grammatical rules to match against the string.
        root: The rule in the ruleset to start searching for.
        tree: When parsed, stores the root node of the AST.
        parsed: Whether the input has been successfully parsed.
    """

    def __init__(self, equation, root="eqn", ruleset=GRAMMAR):
        """Create new parser with input string and options.

        Args:
            equation: See SyntaxParser.equation.
            root: See SyntaxParser.root.
            ruleset: See SyntaxParser.ruleset.
        """
        super(SyntaxParser, self).__init__()
        self.equation = equation
        self.ruleset = ruleset
        self.root = root
        self.tree = None
        self.parsed = False

    def get_tree(self):
        """Get the root node of the AST.
        
        If the equation has not been parsed yet, attempt to do so first.
        
        Returns:
            The root node of the AST.
        """
        if not self.parsed:
            self.tree = self.parse()
        return self.tree

    def parse(self):
        """Attempt to parse the input string.

        Returns:
            The root node of the AST.

        Raises:
            Exception: The input string is not valid.
        """
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
                r"%s|[a-ik-z]|[\d.]*j|[\d.]+" % r"|".join(regex_tokens),
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
        """Attempt to match a set of tokens to a rule.

        Args:
            rule: A key in the ruleset to match against.
            tokens: The list of remaining tokens.

        Returns:
            A Match tuple and the remaining unmatched tokens.
        """
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
        """Reverse associativity on certain binary operators.
        
        The parsing process favours right associativity, which means
        inputs with left-associative operators won't be built into
        correct ASTs. This function fixes the issue by flattening
        subtrees with these operators and re-building left-associative.
        
        Args:
            match: An incorrectly built Match tuple to fix.
            rules: A list of rules representing operators to flip.

        Returns:
            A rebuilt Match tuple.
        """
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
        """Recursively builds an AST from a Match tuple.
        
        Args:
            match: A Match tuple representing the AST to be built.

        Returns:
            The root node of the built AST.
        """
        # Create an alias for the child matches, and
        # force it to be a list.
        matched = match.matched
        if not isinstance(matched, list):
            matched = [matched]

        if match.rule == "NUM":
            # Create a leaf node containing the number.
            return Node(NODE_TYPE_NUM, complex(matched[0]))
        elif match.rule == "VAR":
            # Create a leaf node representing a variable.
            return Node(NODE_TYPE_VAR, matched[0])

        # Delete all child matches that just contain an
        # operator character, since they're useless now.
        i = 0
        while i < len(matched):
            if matched[i].rule not in self.ruleset \
            and matched[i].rule not in FUNCTIONS + ["NUM", "VAR"]:
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
                        NODE_TYPE_OP,
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
                    NODE_TYPE_OP,
                    CODE[match.rule],
                    *[self.build(child) for child in matched])
            else:
                # We just have a container (like sub), so build its child.
                return self.build(matched[0])
        else:
            # We just have a container (like atm).
            return self.build(matched[0])


def recurse(match, func):
    """Apply a function to all matched children in a Match tuple.
    
    Args:
        match: The Match tuple.
        func: The function to apply.

    Returns:
        If the Match tuple is an operator, return a list of the function
        applied on each of its children. Otherwise, return its children.
    """
    if match.rule in GRAMMAR:
        return list(map(func, match.matched))
    else:
        return match.matched
