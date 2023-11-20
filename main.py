import tracemalloc
tracemalloc.start()

import time

import aiohttp

from parser.main_parser import urls, courts, handlers, app
from parser.main_parser.bipium import bipium
from parser.settings.config import Config

import asyncio

if __name__ == '__main__':
    config = Config()
    t1 = time.monotonic()
    s1 = tracemalloc.take_snapshot()
    asyncio.run(app.app(config))
    s2 = tracemalloc.take_snapshot()
    top_stats = s2.compare_to(s1, 'lineno')
    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)
    t2 = time.monotonic()
    print(t2 - t1)
    print('\n\n')
    #630