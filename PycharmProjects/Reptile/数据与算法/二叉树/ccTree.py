class cTree(object):
    def __init__(self,data = None):
        self._data = data
        self.children = []

    def travel(self,node=None,depth = 1):
        if node is None:
            node = self 
        yield (node._data,depth)
        depth += 1 
        for child in node.children:
            yield from self.travel(child,depth)
        depth -= 1

class test_cTree(object):
    def __init__(self):
        self.root = cTree('html')
        head = cTree('head')
        a = cTree('a')
        b = cTree('b')
        head.children.append(a)
        head.children.append(b)
        body = cTree('body')
        x = cTree('x')
        m = cTree('m')
        x.children.append(m)
        body.children.append(x)
        self.root.children.append(head)
        self.root.children.append(body)
        

t = cTree()
a = test_cTree()

for node,depth in  a.root.travel():
    print(node,'depth:',depth)