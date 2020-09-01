import pytest
from page.Main import MainPage

class TestStockSelect:
    @classmethod
    def setup_class(cls):
        cls.stock_select_page = MainPage().stock_select()
        cls.stock_select_page.clear_all()

    @pytest.mark.parametrize('name,code',[(1111,3333),(2222,4444)])
    def test_add_stock(self,name,code):
        assert name in self.stock_select_page.select(code).get_stocks()