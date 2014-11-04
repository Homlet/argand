"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""


TYPE_CIRCLE = 0
TYPE_DISK = 1
TYPE_NEGATIVE_DISK = 2

TYPE_LINE = 3
TYPE_HALF_PLANE = 4

TYPE_RAY = 5
TYPE_SECTOR = 6


class Plot:
    def __init__(self, equation, color=0, alpha=0.0):
        self.equation = equation
        self.color = color
        self.alpha = alpha
        
        self.parse(self.equation)

    def parse(self, equation):
        precedence = {
            "|": 0, "(": 0, ")": 0,
            "+": 1, "-": 1,
            "*": 2,
            "/": 3,
            "^": 4
        }
        def evaluate(stack):
            while precedence[last_operator(stack)] > 0 and len(stack) > 0:
                stack.append([stack.pop() for i in range(3)][::-1])

        def last_operator(stack):
            for c in reversed(stack):
                if c in precedence:
                    return c
        
        terms = []
        ops = []
        for c in equation:
            try:
                # Try to interpret as operator.                    
                if precedence[c] <= precedence[last_operator(stack)]:
                    stack = evaluate(stack)
                stack.append(c)
            except:
                # Otherwise treat as number.
                stack.append(c)
            print(stack)
        i = 0
        while i < len(stack):
            if stack[i] in ["|", "(", ")"]:
                del stack[i]
            i += 1
        print(stack)


if __name__ == "__main__":
    while True:
        plot = Plot(input())
