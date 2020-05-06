import asyncio
import aiohttp
import logging
import time
import json
from aiohttp import ContentTypeError
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

INDEX_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/{id}'
PAGE_SIZE = 18
PAGE_NUMBER = 1
CONCURRENCY = 5

MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECTION_NAME = 'books'

client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection1 = db[MONGO_COLLECTION_NAME]



class Spider(object):
    def __init__(self):
        self.semaphore = asyncio.Semaphore(CONCURRENCY)
        self.collection = ''
        self.error_url = []
        self.session = aiohttp.ClientSession()

    async def getHTML(self,url):
        async with self.semaphore:
            try:
                logging.info('scrape %s',url)
                async with self.session.get(url) as response:
                    logging.info('status code: %s' %response.status)
                    await asyncio.sleep(1)
                    return await response.json()
            except aiohttp.ClientError:
                logging.error('error occurred while running %s',url)
                self.error_url.append(url)
            except ContentTypeError:
                logging.error('error occurred while scraping %s',url, exc_info=True)
                self.error_url.append(url)

    async def requestListPage(self,pageNum):
        url = INDEX_URL.format(offset=pageNum * PAGE_SIZE)
        data = await self.getHTML(url)
        print(type(data))
        logging.info('list data %s'%data)
        await self.saveData(data)
        return data

    async def reqeustDetailPage(self,pageId):
        url = DETAIL_URL.format(id=pageId)
        data = await self.getHTML(url)
        return data
        # await self.saveData(data) 

    async def saveData(self,data):
        logging.info('saving data %s' %data)
        if data:
            await collection1.update_one({'count':data.get('count')},{'$set':data},upsert=True)

    async def main(self):
        self.session = aiohttp.ClientSession()
        listTasks = [asyncio.ensure_future(self.requestListPage(i)) for i in range(1)]
        logging.info('listTasks %s' ,listTasks)
        results = await asyncio.gather(*listTasks)
        print('results',results)
        ids = []
        for result in results:
            # print('result',result)
            if not result:
                continue
            for item in result.get('results'):
                # print('item',item)
                id = item.get('id')
                logging.info(f'id is:{id}')
                ids.append(item.get('id'))
        detailTasks = [self.reqeustDetailPage(id) for id in [30133213,30346157]]
        logging.info('detailTasks %s' ,detailTasks)
        data = await asyncio.wait(detailTasks)
        logging.info(detailTasks)
        await self.session.close()

if __name__ == "__main__":
    s = Spider()
    start_time=time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(s.main())
    end_time=time.time()
    logging.info('cost time %s',end_time-start_time)
    logging.info('error %s',s.error_url)