
class Link():
    def __init__(self,data=None):
        '''
        数据字段和两个链接字段
        '''
        self._data = data
        self.next = None
        self.prev = None
        self.head = None

    def is_empty(self):
        '''
        双向链表
        一种更复杂的链表是“双向链表”或“双面链表”。
        每个节点有两个链接：一个指向前一个节点，当此节点为第一个节点时，指向空值；
        而另一个指向下一个节点，当此节点为最后一个节点时，指向空值。
        '''
        self.head == None

    def add(self,str):
        node = Link(str)
        node.next = self.head
        self.head = node

    def append(self,str):
        '''
        * 链表尾部追加数据
        '''
        item = self
        while item.next is not None:
            item = item.next
        item.next = Link(str)
        return self

    def getOrderList(self):
        item = self
        a = []
        while item is not None:
            a.append(item)
            item = item.next
           
        return a

    def travel(self):
        '''
        * 遍历链表
        '''
        item = self
        a = []
        while item is not None:
            print(item._data)
            a.append(item)
            item = item.next
        return a

    def travel2(self):
        item = self
        while item is not None:
            yield item
            item = item.next

    def serach(self,str):
        '''
        * 查找数据在链表位置
        '''
        item = self
        index = 0
        while item is not None:
            if item._data == str:
                return index
            else:
                index += 1
                item = item.next
        return -1

    def insert(self,pos,str):
        '''
        * 链表特定位置插入数据
        '''
        item =self
        index = 0
        while item is not None:
            if pos == 0 or index == (pos-1):
                break
            index += 1  
            item = item.next
        node = Link(str)

        if pos == 0:
            node.next = item
 
        else:
            node.next = item.next
            item.next = node

    def order(self,str):
        pre = self
        for item in self.travel2():
            if str < item._data:
                break
            pre = item
                
        node = Link(str)
        node.next = pre.next
        pre.next = node
        return self

    def paixu(self):
        index,items = self.travel()
        count = len(items)
        for i in range(count-1):
            for j in range(count-i-1):
                if items[j]._data > items[j+1]._data:
                    items[j],items[j+1] = items[j+1],items[j]
        return items

l = Link(1)
# l.append(10).append(2).append(5)
l.travel()
print(l.serach(3))
print(l.serach(5))
# l.insert(3,3)
# l.travel()
# l.insert(0,0)
# l.travel()
# print(l.paixu())
# for i in l.paixu():
#     print(i._data)
l.travel()
l.add(11)
l.travel()
# l.travel()