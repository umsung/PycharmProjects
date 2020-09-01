import requests
import os
import base64
from APIobject.apiRequest import RequestAPI
from data.ReadData import *

class TestEncode():
    def __init__(self):
        self.req_data = TEST_ENCODE

    def test_api(self):
        ar = RequestAPI()
        data = ar.send(self.req_data)
        assert data['topics']['president'] == 'seveniruby'
        return data


if __name__ == "__main__":
    te = TestEncode()
    print(te.test_api())