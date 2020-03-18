import asyncio

async def do_some_work(x):
    print('waiting',str(x))
    await asyncio.sleep(2)

# async def语句定义的函数为协程函数，调用协程函数，协程并不会开始运行，只是返回一个协程对象
# 让这个协程对象运行的话，有两种方式：
# 在另一个已经运行的协程中用 await 等待它
# 通过 ensure_future 函数计划它的执行
# 简单来说，只有 loop 运行了，协程才可能运行。
# 下面先拿到当前线程缺省的 loop ，然后把协程对象交给 loop.run_until_complete，协程对象随后会在 loop 里得到运行。
loop = asyncio.get_event_loop()
loop.run_until_complete(do_some_work(3))

# run_until_complete 的参数是一个 future，但是我们这里传给它的却是协程对象，
# 之所以能这样，是因为它在内部做了检查，通过 ensure_future 函数把协程对象包装（wrap）成了 future。所以，我们可以写得更明显一些：
loop.run_until_complete(asyncio.ensure_future(do_some_work(3)))

