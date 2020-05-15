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
    # return response

async def request(url):
    print('waiting for',url)
    response =await get(url)
    print('Get response from',url,'response',response)

async def with_get(url):
    print('waiting for',url)
    sem = asyncio.Semaphore(5)  # 限制携程并发量
    timeout = aiohttp.ClientTimeout(total=15)   # 定义超时时间为1s
    async with sem: 
        try:
            # session = aiohttp.ClientSession()
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    # response = await session.get(url)
                    await response.text()
                    # await session.close()
                    print(response.status)
                    # print('body',await response.text())
                    # print('byte',await response.read())
                    # print('json',await response.json())
                    # print('Get response from',url,'response',response)
        except aiohttp.ClientError:
            print('error occurred while runing',url)

if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(with_get(url.format(num=i))) for i in range(1,2)]
    loop.run_until_complete(asyncio.wait(tasks))
    # loop.run_until_complete(asyncio.gather(*tasks))

    end = time.time()

    print('Cost time',end-start)