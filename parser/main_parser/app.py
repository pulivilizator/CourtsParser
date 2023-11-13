import aiohttp

from .bipium.bipium import Bipium
from .handlers import main

async def app(config):
    async with aiohttp.ClientSession() as session:
        bipium = Bipium(config, session)
        await main(config, bipium)

