from queue import Queue
from threading import Thread
from fake_useragent import UserAgent
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from multiprocessing import Process,JoinableQueue


class CrawlInfo(Thread):

    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue
        self.event = threading.Event()

    def run(self):
        headers = {"User-Agent": UserAgent().random}
        while url_queue.empty() == False:
            url = self.url_queue.get()
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                self.html_queue.put(response.text)
                #print(response.text)

    def test(self, url):

        headers = {"User-Agent": UserAgent().random}

        response = requests.get(url, headers=headers)
        print(url_queue.empty() == True)

        if response.status_code == 200:
            self.html_queue.put((url, response.text))
            # print(response.text)


class ParserInfo(Thread):

    def __init__(self,html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while True:
            url, html = self.html_queue.get()
            if html is None:
                break
            html = etree.HTML(html)
            print(url)
            content = html.xpath('//div[@class="content"]/span/text()')

            for info in content:

                print(info)

if __name__ == '__main__':
    url_queue = Queue()
    html_queue = Queue()
    h_queue = JoinableQueue()
    start_url = "https://www.qiushibaike.com/text/page/{}/"
    url_list = [start_url.format(i) for i in range(1, 3)]
    c = CrawlInfo(url_queue, html_queue)
    p = ParserInfo(html_queue)
    with ThreadPoolExecutor(max_workers=2) as excutor:
        excutor.map(c.test, url_list)
        excutor.submit(p.run)
        print(11)
    html_queue.put(None)
    print('主')

    # for i in range(1,3):
    #     new_url = start_url.format(i)
    #     url_queue.put(new_url)
    #     crawl_list = []
    #     paser_list = []
    #     for i in range(0,3):
    #         crawl1 = CrawlInfo(url_queue,html_queue)
    #         crawl_list.append(crawl1)
    #         crawl1.start()
    #     for crawl in crawl_list:
    #         crawl.join()
    #     for i in range(0,3):
    #         paser1 = ParserInfo(html_queue)
    #         paser_list.append(paser1)
    #         paser1.start()
    #     for parser in paser_list:
    #         parser.join()