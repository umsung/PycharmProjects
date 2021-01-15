import multiprocessing
from multiprocessing import Pool, Process
import threading

# 多进程与多线程结合死循环，可把cpu跑到100%
def loop(i):
    x = 0
    print('Thread - ',i)
    while True:
        x = x ^ 1

def proc(i, cpu_cout):
    print('Process: ',i)
    for i in range(cpu_cout*2):
        t = threading.Thread(target=loop, args=(i,))
        t.start()

if __name__ == '__main__':
    cpu_cout = multiprocessing.cpu_count()
    p = Pool(cpu_cout-2)
    for i in range(cpu_cout-2):
        p.apply_async(proc,args=(i, cpu_cout))
    p.close()
    p.join()