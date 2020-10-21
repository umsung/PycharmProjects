class A:
    def isAnagram(self, t, s):
        set_t = set(t)
        set_s = set(s)
        if len(set_t) != len(set_s):
            return False

        for i in set_s:
            if t.count(i) != s.count(i):
                return False
        return True

    def isAnagram2(self, t, s):
        if len(t) != len(s):
            return False

        return sorted(t) == sorted(s)

    def isAnagram3(self, t, s):
        d = {}
        for i in t:
            d[i] = d.get(i, 0) + 1

        for i in s:
            d[i] = d.get(i, 0) - 1

        for i in d.values():
            if i != 0:
                return False
        return True
