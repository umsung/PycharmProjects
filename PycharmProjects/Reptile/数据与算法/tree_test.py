class F():
    def __init__(self,data=None):
        self.data = data
        self.children = []

# a = F(-1)
# a-1 = F(a)
# a-2 = F(a)
# a-3 = F(a)
# a.children.append(a-1)
# a-2-1 = F(a-2)
# a-2-2 = F(a-2)
# a-2-3 = F(a-2)
# (a-2).children.append(a-2-1)

d = {
    "A":"-1",
    "A-1":"A",
    "A-2":"A",
    "A-3":"A",
    "A-2-1":"A-2",
    "A-2-2":"A-2",
    "A-2-3":"A-2"
}

res = []

def fun(node):
    arr.append(node[0])
    if node[1] == '-1':
        return
    fun((node[1],d[node[1]]))


for i in d.items():
    arr = []
    fun(i)
    # print(arr)
    res = arr[::-1]
    res = '/'.join(arr[::-1])
    res = '/'+res
    print(res)