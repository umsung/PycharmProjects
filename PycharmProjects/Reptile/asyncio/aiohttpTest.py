import aiohttp
import asyncio
import time
# aiohttp是一个基于asyncio的异步http网络模块，既可以提供服务端，又可以提供客户端
# 用服务端可以搭建一个支持异步处理的服务器，用于处理请求并返回响应
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

start = time.time()
url = 'https://static4.scrape.cuiqingcai.com/page/{num}'

async def get(url):
    print('waiting for',url)
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()
    await session.close()
    print('Get response from',url,'response',response)
    return response

async def request(url):
    print('waiting for',url)
    response =await get(url)
    print('Get response from',url,'response',response)

async def with_get(url):
    print('waiting for',url)
    timeout = aiohttp.ClientTimeout(total=15)   # 定义超时时间为1s
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            print(response.status)
            # print('Get response from',url,'response',response)

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(with_get(url.format(num=i))) for i in range(1,21)]
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('Cost time',end-start)