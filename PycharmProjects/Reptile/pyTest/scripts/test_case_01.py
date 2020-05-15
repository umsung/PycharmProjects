import pytest


class TestCase(object):

    @pytest.mark.xfail(1 < 2, reason='预期失败， 执行失败')
    def test_case_01(self):
        """ 预期失败， 执行也是失败的 """
        print('预期失败， 执行失败')
        assert 0

    @pytest.mark.xfail(1 < 2, reason='预期失败， 执行成功')
    def test_case_02(self):
        """ 预期失败， 但实际执行结果却成功了 """
        print('预期失败， 执行成功')
        assert 1

    @pytest.mark.xfail(1 > 2, reason='预期成功， 执行成功')
    def test_case_03(self):
        """ 预期成功， 实际执行结果成功 """
        print('预期成功， 执行成功')
        assert 0

    @pytest.mark.xfail(1 > 2, reason='预期成功， 执行失败')
    def test_case_04(self):
        """ 预期成功， 但实际执行结果却失败了 """
        print('预期成功， 执行失败')
        assert 0

    def test_case_05(self):
        """ 普通的测试用例 """
        print('执行成功的普通用例')
        assert 1

    def test_case_06(self):
        """ 普通的测试用例 """
        print('执行失败的普通用例')
        assert 0

    @pytest.mark.parametrize('mobile',[1111,2222])
    def test_case_07(self,mobile):
        assert '手机号码是{}'.format(mobile)

    @pytest.mark.parametrize('mobile',[1111,2222])
    @pytest.mark.parametrize('code',[3333,4444])
    def test_case_08(self,mobile,code):
        assert '手机号码是{},注册码是{}'.format(mobile,code)

    @pytest.mark.parametrize(['mobile','code'],[(1111,3333),(2222,4444)])
    def test_case_09(self,mobile,code):
        assert '手机号码是{},注册码是{}'.format(mobile,code)

if __name__ == '__main__':
    pytest.main(["-s","-v","test_case_01.py"])