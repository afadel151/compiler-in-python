import AST
from AST import addToClass
import parser



@addToClass(AST.Node)
def thread(self,lastNode):
    
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

@addToClass(AST.WhileNode) 
def thread(self, lastNode) :
    lastNode = self.children[0].thread(lastNode)
    lastNode.addNext(self)
    lastfirst=self.children[0]
    while len(lastfirst.children)>0:
        lastfirst=lastfirst.children[0]
    
    self.children[1].addNext(lastfirst)
    lastNode = self.children[1].thread(self)
    
    # print (self, lastNode)
    # for c in self.children:
    #     print ('loop',c)
    #     lastNode = c.thread(lastNode)
    # lastNode.addNext(self)
    return self

def thread(tree) :
    entry = AST.EntryNode() 
    tree.thread ( entry )
    return entry

def read_file(filename):
    with open(filename, 'r') as file:
        f=(file.read()) 
    return f


if __name__ == "__main__":
    from parser import parse 
    import sys, os
    print(len(sys.argv))
    if len(sys.argv) < 2:
        print("Error: missing file argument")
        sys.exit(1)
    filename = sys.argv[1]
    prog =read_file(filename)
    ast = parse(prog)
    entry = thread(ast)
    graph = ast.makegraphicaltree() 
    entry.threadTree ( graph )
    
    
    name = f"ABR/prog.png"
    graph.write_png( name )
    print( "wrote threaded ast to" , name)