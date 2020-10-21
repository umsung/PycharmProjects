
class Solution:
    def reverseListdiedai(self, head):
        """
        遍历链表，指针 cur 指向当前节点，指针 pre 指向 cur 的前驱节点
        初始化 pre 和 cur
        temp 存储 cur 的后继节点
        反转操作，cur 的后继变为前驱
        更新 pre 和 cur，直到 cur 指向空
        :param head:
        :return:
        """
        pre = None
        cur = head

        while cur:
            temp = cur.next
            cur.next = pre
            pre = cur
            cur = temp
        return pre

    def reverseListBydigui(self, head):

        if not head or not head.next:
            return head

        newhead = self.reverseListBydigui(head.next)
        head.next.next = head
        head.next = None
        return newhead

    def reverseListbufen(self, head):
        if not head or not head.next:
            return head

        firstnode = head
        secondnode = head.next

        firstnode.next = self.reverseListbufen(secondnode.next)
        secondnode.next = firstnode
        return secondnode

