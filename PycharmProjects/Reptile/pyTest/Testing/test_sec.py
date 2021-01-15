import pytest


class TestOne:

    def setup(self):
        print('setup')
        print("this is one setUp")

    def test_multi(self,login):
        self.a = login
        print(login)
        assert 6 == 5

    def test_minus(self, login):
        print(self.a + 2)
        assert 6 == 3

    def teardown(self):
        print("this is one teardown")

class TestSec:

    def setup_class(self):
        print("this is second setUp")

    def test_multi(self,login):
        print(login+ 3)
        assert 6 == 9

    def test_minus(self, login):
        assert 6 == 7

    def teardown(self):
        print("this is second teardown")