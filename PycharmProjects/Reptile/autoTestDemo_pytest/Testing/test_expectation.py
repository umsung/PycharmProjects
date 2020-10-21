import pytest


"""
pytest.mark.parametrize装饰器可以实现测试用例参数化。
内置的mark.xfail 标记为失败的用例，预期结果是失败，实际运行也是失败，显示xfailed
"""


class TestExpe:

    @pytest.mark.parametrize('test_input,expect', [
        ("3+5", 8),
        ("2*4", 8),
        pytest.param("6 * 9", 42, marks=pytest.mark.xfail),
    ])
    def test_eval(self, test_input, expect):
        assert eval(test_input) == expect

    @pytest.mark.parametrize("x", [0, 1])
    @pytest.mark.parametrize("y", [2, 3])
    @pytest.mark.parametrize("z", [4, 5])
    def test_foo(self, x, y, z):
        print("参数输出组合%s - %s - %s" %(x, y, z))