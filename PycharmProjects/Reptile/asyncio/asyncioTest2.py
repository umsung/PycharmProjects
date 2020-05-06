import asyncio

# 假如协程是一个 IO 的读操作，等它读完数据后，我们希望得到通知，以便下一步数据的处理。
# 这一需求可以通过往 future 添加回调来实现。

async def do_some_work(x):
    print('waiting',str(x))
    await asyncio.sleep(2)
    return str(x)

def done_callback(futu):
    print('Done',futu)
    print('Done',futu.result())

loop = asyncio.get_event_loop()
futu = asyncio.ensure_future(do_some_work(3))
futu.add_done_callback(done_callback)
print('222',futu)
loop.run_until_complete(futu)
print('1111',futu)