def triangles():
    L = [1]
    n = 0
    while n < 5:
        yield L
        L = [sum(i) for i in zip([0]+L,L+[0])]
        n += 1

f = triangles()
for i in f:
    print(i)

