
# 示例：给定一个数组以及一个窗口的长度 k，现在移动这个窗口，要求打印出一个数组，数组里的每个元素是当前窗口当中最大的那个数。
#
# 输入：nums = [1, 3, -1, -3, 5, 3, 6, 7]，k = 3
#
# 输出：[3, 3, 5, 5, 6, 7]


class Solution:
    def maxSlidingWindow(self, nums, k: int):
        n = len(nums)
        if n == 0:
            return []
        result = []
        temp = max(nums[:k])
        result.append(temp)
        for i in range(n-k):
            if nums[k+i] > temp:
                temp = nums[k+i]
            elif nums[i] == temp:
                temp = max(nums[i+1:i+k+1])
            result.append(temp)
        print(result)

    def maxSlidingWindow2(self, nums, k: int):
        n = len(nums)
        if n == 0:
            return []
        result = []

        for i in range(n-k+1):
            temp = max(nums[i:i+k])
            result.append(temp)
        print(result)

nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
s = Solution()
s.maxSlidingWindow2(nums, k)