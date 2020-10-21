import socket
import threading
import time
from multiprocessing import Pool, Process
import logging
import concurrent.futures
from datetime import datetime

def tcplink(name,ip='47.106.108.100',port=2020):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((ip, port))

    print(s.recv(1024).decode('utf-8'))
    # for data in [b'a', b'b', b'c']:
    #     s.send(data)
    #     print(s.recv(1024).decode('utf-8'))

    # s.send(b'exit')
    # s.close()
    count = 0
    while True:
        # data = input('请输入内容>>：').strip()
        # if not data:
        #     continue
        # s.send(data.encode('utf-8'))
        a = []
        receive = s.recv(1024).decode('utf-8')
        # print(receive)
        count = count + 1
        # print(datetime.now())
        print("心跳次数: ",count)
        logging.info("Thread {}: receive {}".format(name, receive))

        if not receive:
            print('线程{}没有收到心跳包，可能已断开'.format(name))

if __name__ == "__main__":
    ip = '47.106.108.100'
    port = 2020
    # for i in range(2):
    #     tcplink(ip,port)
    # p = Pool(2) # 进程池中进程数量默认是cpu核数
    # p.apply_async(tcplink, args=(ip,port))
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


    with concurrent.futures.ThreadPoolExecutor(max_workers=170) as excutor:
        
        excutor.map(tcplink,range(100))

    # threads=[]
    # for i in range(2):
    #     logging.info("Main    : create and start thread %d.", i)
    #     x = threading.Thread(target=tcplink, args=(ip,port))
    #     threads.append(x)
    #     x.start()

    # for i,thread in enumerate(threads):
    #     logging.info('Main    :before join thread %d' %i)
    #     thread.join()
    #     logging.info('Main    :thread %d done' %i)