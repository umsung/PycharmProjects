import pytest
import sys


# # 使用pytest.skip（reason，allow_module_level = True）跳过整个模块级别
# if not pytest.config.getoption("--custom-flag"):
#     pytest.skip("--custom-flag is missing, skipping tests", allow_module_level=True)
minversion = pytest.mark.skipif(sys.platform == 'win64', reason="atests for win64˓→ only")

@minversion
class TestSkip:

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_skip_uncondition(self):
        print('skip跳过')

    def test_function(self):
        if 1 != 2:
            pytest.skip('在测试执行或设置期间强制跳过pytest.skip（reason）功能')
            print('是否跳过这里2')
        print('是否跳过这里1')

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
    def test_skipif_withConditon(self):
        print('如果条件为True，则此标记将为该每个测试方法生成跳过结果')

    minversion = pytest.mark.skipif(sys.platform == 'win32', reason="atests for win64˓→ only")

    @minversion
    def test_skipif_class(self):
        print('跳过结果')

    def test_skipif_noImport(self):
        pass
