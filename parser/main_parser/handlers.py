from pprint import pp

import aiohttp
from playwright.async_api import async_playwright
import asyncio

from .urls import create_urls
from . import browser_utils
from .html_parser import create_json
from . import url_utils
from .bipium.bipium import Bipium

from fake_useragent import UserAgent
import random


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

async def configurate_browsers(config, browser, urls, bipium):
    pages_count = config.browsers_and_pages['pages']
    urls = url_utils.split_list(urls, pages_count)
    await asyncio.gather(*[parser(browser, url, config, bipium) for url in urls])


async def parser(browser, urls, config, bipium):
    context = await browser.new_context(user_agent=UserAgent().random)
    page = await context.new_page()
    for number, url in urls:
        goto_checker = await browser_utils.page_goto_validator(page, config, url, number, timeout=240000)
        if not goto_checker:
            continue
        page_content = await page.content()
        try:
            lines = create_json(page_content, url, config)
        except Exception as e:
            print(e)
            with open('err.txt', 'a', encoding='utf-8-sig') as f:
                f.write(e)
        resps = await asyncio.gather(*[bipium.write_line(line) for line in lines])
        print(resps)
        # resp = await bipium.write_line(line)
        # print(resp)

#http://sovetsk7.vrn.msudrf.ru/modules.php?name=sud_delo&op=hl&H_date=27.11.2023




async def main(config, bipium):
    urls = await create_urls(config)
    urls = [(ind, url) for ind, url in enumerate(urls)]
    urls = url_utils.split_list(urls, config.browsers_and_pages['browsers'])
    tasks = []
    async with async_playwright() as p:
        browsers = await get_browsers(p, config)
        for index, browser in enumerate(browsers):
            task = asyncio.create_task(configurate_browsers(config, browser, urls[index], bipium))
            tasks.append(task)
        await asyncio.gather(*tasks)


