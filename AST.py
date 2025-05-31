import pydot
class Node:
    count = 0
    type = 'Node (unspecified)'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self,next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result
    
    def __str__(self):
        return self.asciitree()
    
    def __repr__(self):
        return self.type
    
    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape="diamond"))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
            return dot
        
    def threadTree(self, graph, seen = None, coul=0):
            colors = ('black', 'red', 'red', 'red', 'red', 'red')
            if not seen: seen = []
            if self in seen: return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graphnode = pydot.Node(self.ID,label=repr(self), shape="diamond")
                graphnode.set_style('dotted')
                graph.add_node(graphnode)
            label = len(self.next)-1
            for i,c in enumerate(self.next):
                if not c: return
                coul = (coul + 1) % len(colors)
                color = colors[coul]
                c.threadTree(graph, seen, coul)
                edge = pydot.Edge(self.ID,c.ID)
                edge.set_color(color)
                edge.set_arrowsize('0.8')
                edge.set_constraint('false') 
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph    


class ProgramNode(Node):
    type = 'Program'
        
class TokenNode(Node):
    type = 'token'
    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok
        
    def __repr__(self):
        return repr(self.tok)

class BlockNode(Node):
    type = 'Block'

class BinOpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self,children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1
        
    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)
    
class FunctionNode(Node):
    def __init__(self, name, children):
        Node.__init__(self,children)
        self.name = name
        
    def __repr__(self):
        return "%s" % (self.name)

class ReturnNode(Node):
    type = 'return'

class AssignNode(Node):
    type = '='
    
class PrintNode(Node):
    type = 'print'
    
class WhileNode(Node):
    type = 'while'

class IfElseNode(Node):
    type = 'if-else'

class ReadNode(Node):
    type = 'read'
    
class EntryNode(Node):
    type = 'ENTRY'
    def __init__(self):
        Node.__init__(self, None)



def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator