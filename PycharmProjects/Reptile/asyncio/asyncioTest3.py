import asyncio

# 多个协程，同时在一个 loop 里运行
# gather 或 with 起聚合的作用，把多个 futures 包装成单个 future，也可把多个协程直接合并成一个 future，因为 loop.run_until_complete 只接受单个 future。
async def do_some_work(x):
    print('waiting',str(x))
    await asyncio.sleep(2)
    
coros = [do_some_work(i) for i in range(1,4)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(coros))

# loop.run_until_complete(asyncio.gather(do_some_work(1), do_some_work(3)))

# 传多组futures也可以
# loop.run_until_complete(asyncio.gather(asyncio.ensure_future(do_some_work(1)),
            #  asyncio.ensure_future(do_some_work(3))))
# 效果等于
# loop.run_until_complete(asyncio.gather(do_some_work(1),
            #  do_some_work(3)))