import time
from datetime import datetime
import re


class GetTime(object):
    def get_system_time(self):
        print(time.time())
        now = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        return now

    def parse_time(self, datetime):
        if re.match('\d+月\d+日', datetime):
            datetime = time.strftime('%Y年', time.localtime()) + datetime
        if re.match('\d+分钟前', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y年%m月%d日 %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('今天.*', datetime):
            datetime = re.match('今天(.*)', datetime).group(1).strip()
            datetime = time.strftime('%Y年%m月%d日', time.localtime()) + ' ' + datetime
        return datetime

gettime = GetTime()
print(gettime.get_system_time())
print(str(datetime.now()))