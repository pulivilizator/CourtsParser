import time

import aiohttp

from parser.main_parser import urls, courts, handlers, app
from parser.main_parser.bipium import bipium
from parser.settings.config import Config

import asyncio
#3239

if __name__ == '__main__':
    config = Config()
    t1 = time.monotonic()
    asyncio.run(app.app(config), debug=True)
    t2 = time.monotonic()
    print(t2 - t1)
    print('\n\n')