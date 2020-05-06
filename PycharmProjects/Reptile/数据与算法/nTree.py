class nTree(object):
    def __init__(self,data=None):
        self.data = data
        self.left = None
        self.right = None

    @classmethod
    def travel(cls,subtree):
        if subtree is None:
            return
        # 前序  中序  后序
        cls.travel(subtree.left)
        print(subtree.data)
        cls.travel(subtree.right)

    @classmethod
    def deepth(cls,subtree,depth):
        if subtree is None:
            return depth
        
        max_left = cls.deepth(subtree.left,depth+1)
        max_right = cls.deepth(subtree.right,depth+1)
        return max_left if max_left > max_right else max_right

class test_nTree(object):
    def __init__(self):
        self.tree = nTree(0)
        self.tree.left = nTree(1)
        self.tree.right = nTree(2)
        self.tree.left.left = nTree(3)
        self.tree.left.right = nTree(4)
        self.tree.left.right.left = nTree(5)
        self.tree.left.right.right = nTree(6)
        self.tree.left.right.left.left = nTree(7)

    def test_travel(self):
        return nTree.travel(self.tree)

    def test_deepth(self):
        return nTree.deepth(self.tree,0)

t = test_nTree()
t.test_travel()
print(t.test_deepth())