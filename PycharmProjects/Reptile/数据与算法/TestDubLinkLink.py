class Link(object):
    def __init__(self,item = None):
        self.item = item
        self.next = None
        self.prev = None

class DLinkList(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head == None

    def travel(self):
        if self.is_empty():
            return
        cur = self._head
        while cur is not None:
            print(cur.item)
            cur = cur.next

    def length(self):
        cur = self._head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def search(self,item):
        cur = self._head
        count = 0
        while cur is not None:
            if cur.item == item:
                print(count)
                return True
            count += count
            cur = cur.next
        return False

    def add(self,item):
        node = Link(item)
        if self.is_empty():
            self._head = node
        else:
            cur = self._head
            node.next = self._head
            self._head.prev = node
            self._head = node

    def append(self,item):
        node = Link(item)
        if self._head is None:
            self._head = node
        else:
            cur = self._head
            while cur.next is not None:
                cur = cur.next
            # node.next = cur.next 
            cur.next = node
            node.prev = cur

    def insert(self,pos:int,item):
        if pos <= 0:
            self.add(item)
        elif pos > (self.length()-1):
            self.append(item)
        else:
            index = 0
            cur = self._head
            while index < pos-1:
                cur = cur.next
                index += 1
            node = Link(item)
            node.next = cur.next
            node.prev = cur
            cur.next = node

    def remove(self,item):
        cur = self._head
        while cur is not None:
            if cur.item == item:
                if cur == self._head:
                    self._head = cur.next
                    if cur.next:
                        cur.next.prev = None
                else:
                    cur.prev.next = cur.next
                    if cur.next:
                        cur.next.prev = cur.prev
            else:
                cur = cur.next

    def update(self,index,item):
        if self.is_empty():
            pass
        elif index <= 1:
            self._head.item = item
        elif index > (self.length()-1):
            cur = self._head
            count = 0
            while cur.next is not None:
                cur = cur.next
            cur.item = item
        else:
            cur = self._head
            count = 0
            while cur.next is not None:
                if count == index-1:
                    break
                count += 1
                cur = cur.next
            cur.item = item


if __name__ == "__main__":
    D = DLinkList()
    print(D._head)
    D.travel()
    print(D.length())
    D.insert(11,3)
    D.insert(-1,30)
    D.add(22)
    D.append(55)
    D.update(0,1)
    D.update(3,3)
    D.update(2,6)
    D.travel()
    print(D.length())