import requests
from API_Auto_yoyo.common.logger import Log


class blog():
    def __init__(self, s):
        self.s = s
        self.head = ''
        self.url = ''

    def login(self):
        try:
            s = requests.post(self.url, self.head)
            if s.status_code == 200:
                return s
        except ConnectionError as e:
            print(e)

