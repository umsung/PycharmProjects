import pytest
import sys

print(sys.path)

# @pytest.fixture(autouse=True)  # 设置为默认运行
# def before():
#     print("------->before")

@pytest.fixture(scope="session")  # 设置为session级别，需要应用才会运行
def before():
    print("------->before")

class Test_ABC:
    def setup(self):
        print("------->setup")

    def test_a(self):
        print("------->test_a")
        assert 1
        
    def test_b(self):
        print("------->test_b")
        assert 1

    @pytest.mark.skip(condition='我就是要跳过这个用例啦')
    def test_case_01():
        assert 1

    @pytest.mark.skipif(condition=1 < 2, reason='如果条件为true就跳过用例')
    def test_case_02():
        assert 1

if __name__ == '__main__':
    pytest.main(["-s","-v","test_fixture.py"])

    # -s，表示输出用例执行的详细结果。
    # test_fixture.py是要执行的脚本名称   命令行 python -s test_fixture.py