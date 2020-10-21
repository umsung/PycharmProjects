array = [[1,8,5,2],
         [4,1,7,3],
         [3,6,2,9]]


rowCount = len(array)
columnCount = len(array[0])

dp = [[0 for i in range(columnCount)] for j in range(rowCount)]

for x in range(rowCount):
    for y in range(columnCount):
        if x == 0:
            dp[x][y] = array[x][y]
        elif y == 0:
            dp[x][y] = array[x][y] + min(dp[x-1][y],dp[x-1][y+1])
        elif y == columnCount - 1:
            dp[x][y] = array[x][y] + min(dp[x-1][y-1],dp[x-1][y])
        else:
            dp[x][y] = array[x][y] + min(dp[x-1][y-1],dp[x-1][y],dp[x-1][y+1])

print(min(dp[-1]))































x = len(array)
y = len(array[0])
dp = [[0 for i in range(y)] for j in range(x)]
# 遍历顺序是每行内的每列。所以遍历array中第一行只执行到if，dp中第一行就确定了，然后再确定dp第二行。
# 要注意两个边界条件
for i in range(x):
    for j in range(y):
        if i == 0:
            dp[i][j] = array[i][j]
        elif j == 0:
            dp[i][j] = array[i][j] + min(dp[i-1][j], dp[i-1][j+1])
        elif j == y-1:
            dp[i][j] = array[i][j] + min(dp[i-1][j-1],dp[i-1][j])
        else:
            dp[i][j] = array[i][j] + min(dp[i-1][j-1],dp[i-1][j],dp[i-1][j+1])

# [[1, 8, 5, 2], 
#  [5, 2, 9, 5], 
#  [5, 8, 4, 14]]
print(min(dp[-1]))