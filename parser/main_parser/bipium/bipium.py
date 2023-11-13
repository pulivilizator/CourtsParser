import asyncio

import aiohttp

from .authorization import get_auth_cookie


class Bipium:

    def __init__(self, config, session: aiohttp.ClientSession):
        self.config = config
        self.headers = get_auth_cookie(config)
        self.catalog_url = f'https://{self.config.bipium_domain}.bpium.ru/api/v1/catalogs/{self.config.bipium_catalog}/records'
        self.session = session

    async def write_line(self, line):
        resp = await self.session.post(self.catalog_url, headers=self.headers, json=line)
        await asyncio.sleep(1)
        return resp.status


    async def create_table(self):
        pass