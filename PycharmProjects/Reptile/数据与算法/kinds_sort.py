

class sortKind(object):
    def __init__(self):
        self.data = [3,1,5,4,2]
        self.sort_data = [1,2,3,4,5]

    def setup(self):
        self.data = [2,1,5,4,3]
        self.sort_data = [1,2,3,4,5]

    def bubble_sort(self):
        count = len(self.data)
        for i in range(0,count-1):
            for j in range(0,count-i-1):
                if self.data[j] > self.data[j+1]:
                    self.data[j],self.data[j+1] = self.data[j+1],self.data[j]
        return self.data

    def selector_sort(self):
        count = len(self.data)
        for i in range(count-1):
            minIndex = i
            for j in range(i+1,count):
                if self.data[minIndex] > self.data[j]:
                    minIndex = j
            self.data[i],self.data[minIndex] = self.data[minIndex],self.data[i]
        return self.data

    def quick_sort(self,data):
        if len(data) < 2:
            return data
        midNum = data[len(data)//2]
        left = [i for i in data if midNum>i]
        mid = [i for i in data if midNum == i]
        right = [i for i in data if midNum < i]
        return self.quick_sort(left) + mid + self.quick_sort(right)

    def test_sort(self):
        assert self.sort_data == self.bubble_sort()

s = sortKind()
# print(s.data)
# print(s.bubble_sort())
# print(s.data)
# print(s.selector_sort())
print(s.data)
print(s.quick_sort(s.data))
s.test_sort()