import AST
from AST import addToClass
import os
@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self
@addToClass(AST.WhileNode)
def thread(self, lastNode):
    conditionNode = self.children[0]
    bodyNode = self.children[1]
    lastNode = conditionNode.thread(lastNode)
    conditionNode.addNext(self)
    lastNode = bodyNode.thread(self)
    return self

@addToClass(AST.IfElseNode)
def thread(self, lastNode):
    conditionNode = self.children[0]
    ifBlockNode = self.children[1]

    lastNode = conditionNode.thread(lastNode)
    conditionNode.addNext(self)

    lastNode = ifBlockNode.thread(self)
    
    if not lastNode.next:
        lastNode.addNext(self) 

    if len(self.children) > 2:
        elseBlockNode = self.children[2]
        lastNode = elseBlockNode.thread(self)

        if not lastNode.next:
            lastNode.addNext(self) 

    return self
def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

if __name__ == "__main__":
    from parse import parse
    import sys, os
    prog = read_file(sys.argv[1])
    ast, output = parse(prog)
    entry = thread(ast)
    graph = ast.makegraphicaltree()
    entry.threadTree(graph)
    name = os.path.basename(os.path.splitext(sys.argv[1])[0]) + 'ABR_GENERATED.png'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    trees_dir = os.path.join(current_directory, "ABR/")
    os.makedirs(trees_dir, exist_ok=True)
    graph.write_png(os.path.join(trees_dir, name))
    print("wrote threaded ast into", name)
 