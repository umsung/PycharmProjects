import pytest
from page.MallMain import *
import yaml

class TestSearch:

    @classmethod
    def setup_class(cls):
        cls.mall = MainPage()
        cls.search_page = cls.mall.search()

    @pytest.mark.paramstrzie('keyword', yaml.safe_load(open('../data/keyword.yaml', encoding='utf-8')))
    def test_search(self, keyword):
        # assert self.search_page.search('test').get_price() > 100
        assert self.search_page.search_by(keyword).get_price() > 100

    def teardown(self):
        self.mall.back()

    def teardown_class(self):
        self.search_page.close()

