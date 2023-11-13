import aiohttp
from aiohttp_socks import ProxyConnector, ProxyType
import asyncio

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import itertools

from ..settings import settings
from . import url_utils


def get_urls(regions_and_cities):
    urls = []
    for region in regions_and_cities:
        cities = regions_and_cities[region]
        if not cities:
            cities = ['']
        for city in cities:
            urls.append(settings.FORMAT_REGIONS_URL.format(url_utils.region_decoder(region), url_utils.city_decoder(city)))

    return urls

async def get_hrefs(proxy, url, semaphore):
    headers = {'user-agent': UserAgent().random}
    connector = None
    if proxy:
        connector = ProxyConnector(
                    proxy_type=ProxyType.HTTP,
                    host=proxy['server'],
                    port=proxy['port'],
                    username=proxy['username'],
                    password=proxy['password'],
                    rdns=True
                )
    async with semaphore:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers) as response:
                text = await response.read()
                soup = BeautifulSoup(text, 'html.parser')
                courts_list = [i.text for i in soup.find_all('a', target='_blank')]
                await asyncio.sleep(1)
                return courts_list

def get_all_courts():
    ua = UserAgent()
    url = settings.ALL_REGIONS_URL
    headers = {'user-agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    courts_list = [i.text for i in soup.find_all('a', target='_blank')]
    courts = list(filter(lambda x: all(reg not in x for reg in settings.NOT_PARSING_URLS), courts_list))

    return courts



async def get_processing_urls(config):
    regions_and_cities = config.regions_and_cities
    if not regions_and_cities:
        courts_urls = get_all_courts()
    else:
        proxies = config.proxies
        semaphore = asyncio.BoundedSemaphore(config.semaphore)
        tasks = []
        urls = get_urls(regions_and_cities)

        count = 0
        for proxy in itertools.cycle(proxies):
            if not proxies:
                proxy = None
            task = asyncio.create_task(get_hrefs(proxy, urls[count], semaphore))
            tasks.append(task)
            count += 1
            if count == len(urls):
                break

        courts_urls = await asyncio.gather(*tasks)
        courts_urls = set(itertools.chain.from_iterable(courts_urls))
    return sorted(sorted(courts_urls, key=lambda x: x.split('.')[1]), key=lambda x: x.split('.')[0])
