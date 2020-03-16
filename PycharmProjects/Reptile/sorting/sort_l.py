# 冒泡排序，比较相邻两个元素 ，如果第一个比第二个大，就交换他们两个

def bubbleSort(arr):
    for i in range(1,len(arr)):
        for j in range(0,len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


# 选择排序
def selectSort(arr):
    for i in range(len(arr)-1):
        
        minIndex = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        
        if i != minIndex:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr


def insertSort(arr):
    for i in range(len(arr)):
        firstIndex = i-1
        current = arr[i]
        while firstIndex >= 0 and arr[firstIndex]> current:
            arr[firstIndex+1] = arr[firstIndex]
            firstIndex -=1

        arr[firstIndex+1]=current


if __name__ == "__main__":
    
    print(bubbleSort([1,6,9,5,1]))
    print(selectSort([1,6,9,5,1]))

