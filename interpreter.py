from AST import addToClass
from functools import reduce
import AST
from parser import parse
import sys

operations = {
        '+': lambda x, y: x+y,
        '-': lambda x, y: x-y,
        '*': lambda x, y: x*y,
        '/': lambda x, y: x / y,
        '&' : lambda x, y : x & y,
        '|' : lambda x, y : x|y,
        '<' : lambda x, y : x < y,
        '>' : lambda x, y : x > y,
        '>=' : lambda x, y: x >= y,
        '<=' : lambda x, y: x <= y,
        '==' : lambda x, y: x == y,
        '!=' : lambda x, y: x != y
}

vars = {}


@addToClass(AST.ProgramNode)
def execute(self):
   
    for c in self.children:
        c.execute()


@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str) and not self.tok.startswith('\''):
        try:
            return vars[self.tok] 
        except KeyError:
            print( f"∗∗∗ Error: variable {self.tok} undefined!")  
    return self.tok


@addToClass( AST.WhileNode ) 
def execute(self):
    while bool(self.children[0].execute()):
        self.children[1].execute()

@addToClass( AST.IfNode ) 
def execute(self):
    if bool(self.children[0].execute()):
        self.children[1].execute()
    elif len(self.children) > 2:
        self.children[2].execute()
    
    
@addToClass( AST.OpNode ) 
def execute(self):
    
    args = [c.execute() for c in self.children] 
    if len(args) == 1:
        result = not self.children[0].execute()
    else:
        result = reduce(operations[self.op] , args)
    
    return result


@addToClass( AST.AssignNode ) 
def execute(self) :
    vars[self.children[0].tok] = self.children[1].execute()
    
@addToClass( AST.PrintNode ) 
def execute(self) :
    print(self.children[0].execute())

@addToClass( AST.ReadNode ) 
def execute(self) :
    print("Entrer une valeur \n")
    a = input()
    a = int(a)
    vars[self.children[0].tok] = a



def read_file(filename):
    with open(filename, 'r') as file:
        f = (file.read())
    return f


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Error: missing file argument")
        sys.exit(1)
    filename = sys.argv[1]
    prog = read_file(filename)    
    ast = parse(prog)
    ast.execute()   