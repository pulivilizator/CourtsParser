import logging

from playwright.async_api import async_playwright
import asyncio
import aiohttp

from .urls import create_urls
from . import browser_utils
from . import url_utils
from .writer import write

from collections import namedtuple
import random
from fake_useragent import UserAgent

links_data = namedtuple('links_data', ['index', 'court_name', 'url', 'address'])

async def get_browsers(p, config):
    browsers = []
    proxies = config.proxies
    browsers_count = config.browsers_and_pages['browsers']

    for i in range(browsers_count):
        proxy = None
        if proxies[0]:
            proxy = {
                    "server": f"{proxies[i]['server']}:{proxies[i]['port']}",
                    "username": proxies[i]['username'],
                    "password": proxies[i]['password']
                    }
        browser = await p.chromium.launch(
            headless=config.headless,
            proxy=proxy
        )
        browsers.append(browser)
    return browsers

async def configurate_browsers(config, browser, urls, writer):
    pages_count = config.browsers_and_pages['pages']
    urls = url_utils.split_list(urls, pages_count)
    await asyncio.gather(*[parser(browser, url, config, writer) for url in urls])

async def parser(browser, urls: list[links_data], config, writer):
    context = await browser.new_context(user_agent=UserAgent().random)
    await asyncio.sleep(random.randint(1, 5))
    page = await context.new_page()
    async with aiohttp.ClientSession() as captcha_session:
        for link_data in urls:
            print(link_data.url)
            logging.info(f'HANDLERS::EVENTLOOP:{asyncio.get_event_loop()}::URL:{link_data.url}::STATUS:OPEN')
            goto_checker = await browser_utils.page_goto_validator(page, config, link_data.url, link_data.index, captcha_session, timeout=90000)
            if not goto_checker:
                continue
            try:
                await write(page, link_data, config, writer)
            except Exception as e:
                print(f'HANDLERS::ERROR_WRITE:{e}::URL:{link_data.url}')
                logging.warning(f'HANDLERS::ERROR_WRITE:{e}::URL:{link_data.url}')
                continue
            logging.info(f'HANDLERS::EVENTLOOP:{asyncio.get_event_loop()}::URL:{link_data.url}::STATUS:FINISHED')

        await page.close()


async def main(config, writer):
    urls = await create_urls(config)
    urls = [links_data(index=ind, court_name=url[0], url=url[1], address=url[2]) for ind, url in enumerate(urls)]
    urls = url_utils.split_list(urls, config.browsers_and_pages['browsers'])
    tasks = []
    async with async_playwright() as p:
        browsers = await get_browsers(p, config)
        if len(browsers) > len(urls):
            browsers = browsers[:len(urls)]
        for index, browser in enumerate(browsers):
            task = asyncio.create_task(configurate_browsers(config, browser, urls[index], writer))
            tasks.append(task)
        await asyncio.gather(*tasks)


