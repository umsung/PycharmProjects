from SourceCode.sec import Second


class TestSec:

    def setup_class(self):
        self.sec = Second()

    def test_multi(self):
        assert 6 == self.sec.multi(2, 3)

    def test_minus(self, login):
        assert 6 == self.sec.minus(9, 3)
