import tracemalloc
from datetime import datetime

tracemalloc.start()

import time

from parser.main_parser import app
from parser.settings.config import Config

import asyncio
import logging

from playwright import async_api

async def p():
    config = Config()
    async with async_api.async_playwright() as p:
        for i in config.proxies[:1]:
            proxy = {
                "server": f"{i['server']}:{i['port']}",
                "username": i['username'],
                "password": i['password']
            }
            browser = await p.chromium.launch(headless=False, proxy=proxy)
            c = await browser.new_context()
            pag = await c.new_page()
            await pag.goto('http://severny.komi.msudrf.ru/modules.php?name=sud_delo&op=hl&H_date=29.11.2023')
            for _ in range(10):
                await pag.reload()
                time.sleep(2)
            time.sleep(10)
            await pag.close()

def main_parser(config):
    try:
        t1 = time.monotonic()
        s1 = tracemalloc.take_snapshot()
        asyncio.run(app.app(config))
        s2 = tracemalloc.take_snapshot()
        top_stats = s2.compare_to(s1, 'lineno')
        memory = '[ 10 Наибольших потребителей памяти ]\n'
        for stat in top_stats[:10]:
            memory += f'{stat}\n'
        logging.info(f'MAIN::{memory}')
        t2 = time.monotonic()
        logging.info(f'MAIN::ВРЕМЯ РАБОТЫ ПРОГРАММЫ {t2 - t1} сек.\n\n')
        print(f'MAIN::ВРЕМЯ РАБОТЫ ПРОГРАММЫ {t2 - t1} сек.\n\n')
        return True
    except Exception as e:
        print(e)
        print(type(e))
        logging.critical(f'MAIN::ERROR_TYPE:{type(e)}::ERROR_DESCRIPTION:{e}\n\n')
        return False



if __name__ == '__main__':
    while True:
        config = Config()
        if config.start_now or (datetime.now().strftime('%H:%M') in config.start_time and config.check_dates) and datetime.now() < datetime.fromisoformat('2024-01-01 00:00:00'):
            logging.basicConfig(level=logging.INFO, filename=f'logs/{datetime.now().strftime("%Y-%m-%d")}.log',
                                filemode='a', format="%(asctime)s %(levelname)s %(message)s")
            c = 1
            while True:
                logging.info(f"MAIN::START PARSER:{c}/3")
                result = main_parser(config)
                if result:
                    time.sleep(60)
                    break
                else:
                    if c == 3:
                        logging.critical(f'MAIN::STOP PROGRAM')
                        break
                    c += 1
                    time.sleep(60)
        else:
            print(f'Программа ожидает запуск\nРасписание запуска: {", ".join(config.start_time)}')
            time.sleep(5)