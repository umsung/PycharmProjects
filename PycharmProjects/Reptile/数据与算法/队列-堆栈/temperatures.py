
# 给定 T：[23, 25, 21, 19, 22, 26, 23]
# 返回 D:  [  1,   4,   2,   1,   1,   0,   0]


class Solution:
    def dailyTemperatures(self, T):
        result = [0] * len(T)
        d = {}
        for i in range(len(T)):
            d[T[i]] = i
            temp = [j for j in range(i+1, len(T)) if T[j] > T[i]]
            result[i] = min(temp) - i if temp else 0
        print(result)
        return result

    def dailyTemperatures2(self, T):
        result = [0] * len(T)
        stack = []
        for i in range(len(T)):
            while stack and T[i] > T[stack[-1]]:
                result[stack[-1]] = i - stack[-1]
                stack.pop()
            stack.append(i)
        print(result)

s = Solution()
T = [23, 25, 21, 19, 22, 26, 23]
s.dailyTemperatures2(T)