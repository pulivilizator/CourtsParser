import aiohttp
import aiofiles
import aiocsv
import csv

from .bipium.bipium import Bipium
from .handlers import main
from .csv_writer import CsvWriter
from ..settings import settings

async def app(config):
    csv_or_bipium = config.writer
    if csv_or_bipium == 'bipium':
        async with aiohttp.ClientSession() as session:
            bipium = Bipium(config, session)
            await main(config, bipium)

    elif csv_or_bipium == 'excel':
        with open('results.csv', 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(settings.CSV_TITLES)
        async with aiofiles.open('results.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = aiocsv.AsyncWriter(file, delimiter=';')
            csv_writer = CsvWriter(writer)
            await main(config, csv_writer)

