from bs4 import BeautifulSoup as bs
import requests
import asyncio
import aiofiles
import aiohttp
import pandas as pd
import async_timeout
from io import StringIO
import re

data_path = 'stock_analyzer/tickers.csv'
sem = asyncio.Semaphore(20)

async def read_csv():
    async with aiofiles.open(data_path, mode='r', encoding='latin1') as f:
        contents = await f.read()
    data = StringIO(contents)
    df = pd.read_csv(data, sep=',')
    return df

df = asyncio.run(read_csv())

info_dict = df.to_dict(orient='records')
tickers = [list(stock.values())[0] for stock in info_dict]
prices = []


def getPossibleResults(stock_name):
    possible_result_ticker = list(stock['Ticker'] for stock in info_dict if re.search(stock_name, str(stock['Name']), flags=re.IGNORECASE))  # noqa: E501
    possible_result_name = list(stock['Name'] for stock in info_dict if re.search(stock_name, str(stock['Name']), flags=re.IGNORECASE))  # noqa: E501
    stocks = accessStockPage(possible_result_ticker)
    return possible_result_ticker, possible_result_name, stocks

def accessStockPage(results):
    stocks = []
    for i in range(len(results) - 1):
        stock_page = 'https://finance.yahoo.com/quote/{}?p={}&'.format(results[i], results[i])
        stocks.append(stock_page)
    return stocks

async def getPrice(text):
    soup = bs(text, "html.parser")
    price = soup.find_all('div', {'class': "My(6px) Pos(r) smartphone_Mt(6px)"})[0].find('span').text
    prices.append(price)
    # print(price, type(price))

async def getUrl(url):
    async with aiohttp.ClientSession() as s:
        with async_timeout.timeout(10):
            async with s.get(url) as response:
                text = await response.text()
                return text

async def crawler(url):
    with(await sem):
        text = await getUrl(url)
        await getPrice(text)

def crawl(stock_name):
    stocks = getPossibleResults(stock_name)[2]
    tasks = []
    for i in range(len(stocks) - 1):
        tasks.append(crawler(stocks[i]))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return prices

if __name__ == "__main__":
  
    crawl('facebook')
