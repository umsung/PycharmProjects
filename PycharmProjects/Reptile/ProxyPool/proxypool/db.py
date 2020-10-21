import redis
from PycharmProjects.Reptile.ProxyPool.proxypool.error import PoolEmptyError
from PycharmProjects.Reptile.ProxyPool.proxypool.setting import HOST, PORT, PASSWORD


class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        get proxies from redis  取出count个proxy以列表形式返回，相当于从redis中剪切出来
        """
        proxies = self._db.lrange("proxies", 0, count - 1)  # lrange 只返回指定区间的元素
        self._db.ltrim("proxies", count, -1)  # ltrim 返回指定区间的元素，不在范围内的将被移除redis
        return proxies

    def put(self, proxy):
        """
        add proxy to right top
        """
        self._db.rpush("proxies", proxy)  # rpush将value插入列表proxies的尾部

    def pop(self):
        """
        get proxy from right.
        """
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen("proxies")

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())