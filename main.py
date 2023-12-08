import tracemalloc
from datetime import datetime

tracemalloc.start()

import time

from parser.main_parser import app
from parser.settings.config import Config

import asyncio
import logging

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
        if config.start_now or (datetime.now().strftime('%H:%M') in config.start_time and config.check_dates):
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