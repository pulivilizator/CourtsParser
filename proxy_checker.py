import time
from datetime import datetime

from parser.settings.config import Config

import logging
import asyncio
from playwright import async_api

async def p():
    config = Config()
    logging.basicConfig(level=logging.INFO, filename=f'logs/proxy_checker_results.log',
                        filemode='w', format="%(asctime)s %(levelname)s %(message)s")
    async with async_api.async_playwright() as p:
        for i in config.proxies:
            proxy = {
                "server": f"{i['server']}:{i['port']}",
                "username": i['username'],
                "password": i['password']
            }
            logging.info(f'INFO:CHECK: {proxy}')
            print(f'Проверяю {proxy}')
            try:
                browser = await p.chromium.launch(headless=False, proxy=proxy)
                c = await browser.new_context()
                pag = await c.new_page()
                await pag.goto('http://severny.komi.msudrf.ru/modules.php?name=sud_delo&op=hl&H_date=29.11.2023')
                for _ in range(5):
                    await pag.reload()
                    time.sleep(1)
                time.sleep(10)
                await pag.close()
                print(f'Прокси {proxy} успешно завершил проверку')
                logging.info(f'INFO:FINISH: {proxy}')
                print()
            except Exception as e:
                print()
                logging.warning(f'WARNING:PROXY ERROR: {proxy}')
                print(f'С прокси {proxy} произошла ошибка: {e}')
                print()
                time.sleep(5)
                await pag.close()
                continue

if __name__ == '__main__':
    asyncio.run(p())
    while True:
        time.sleep(99999)