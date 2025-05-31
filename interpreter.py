import AST
from functools import reduce
import re

class Executor:
    def __init__(self):
        self.vars = {}
        self.operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '|': lambda x, y: x or y,
            '&': lambda x, y: x and y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y
        }

    def execute(self, node):
        method_name = 'execute_' + type(node).__name__
        method = getattr(self, method_name, self.generic_execute)
        return method(node)

    def generic_execute(self, node):
        raise Exception(f'No execute_{type(node).__name__} method')

    def execute_ProgramNode(self, node):
        for child in node.children:
            if child.name.tok == 'main':
                self.execute(child)

    def execute_FunctionNode(self, node):
        self.execute(node.children[0])

    def execute_BlockNode(self, node):
        for child in node.children:
            self.execute(child)

    def execute_TokenNode(self, node):
        if isinstance(node.tok, str):
            try:
                return self.vars[node.tok]
            except KeyError:
                if re.match(r"'.*'", node.tok):
                    return node.tok.replace("'", "")
                else:
                    print(f"*** Error: variable {node.tok} undefined!")
        return node.tok

    def execute_BinOpNode(self, node):
        args = [self.execute(child) for child in node.children]
        if len(args) == 1:
            if node.op == "!":
                return not self.execute(node.children[0])
            else:
                args.insert(0, 0)
        return reduce(self.operations[node.op], args)

    def execute_AssignNode(self, node):
        self.vars[node.children[0].tok] = self.execute(node.children[1])

    def execute_PrintNode(self, node):
        print(self.execute(node.children[0]))

    def execute_ReadNode(self, node):
        user_input = input("Enter a value: ")
        try:
            value = int(user_input)
            self.vars[node.children[0].tok] = value
        except ValueError:
            print("Invalid input. Expected an integer.")

    def execute_WhileNode(self, node):
        while self.execute(node.children[0]):
            self.execute(node.children[1])

    def execute_IfElseNode(self, node):
        if self.execute(node.children[0]):
            self.execute(node.children[1])
        elif len(node.children) > 2:
            self.execute(node.children[2])

    def execute_ReturnNode(self, node):
        return self.execute(node.children[0])

    def execute_FunctionCallNode(self, node):
        func_name = node.name.tok
        args = [self.execute(arg) for arg in node.children]
        if func_name in functions:
            return functions[func_name](*args)
        else:
            print(f"*** Error: function {func_name} undefined!")
            return None

# Dictionary to store function definitions
functions = {}

# Function to read file contents
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

if __name__ == "__main__":
    from parse import parse
    import sys

    # Read the program file specified as the first argument
    prog = read_file(sys.argv[1])
    ast, output = parse(prog)

    # Execute the AST
    executor = Executor()
    executor.execute(ast)
