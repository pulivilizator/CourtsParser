from pprint import pp

from .url_utils import get_addresses
from .courts import get_processing_urls


async def create_urls(config):
    processed_urls = await get_processing_urls(config)
    dates = config.dates
    addresses = get_addresses()
    urls = [(name, url + '/modules.php?name=sud_delo&op=hl&H_date=' + date)
            if url[-1] != '/'
            else (name, url[:-1] + '/modules.php?name=sud_delo&op=hl&H_date=' + date)
            for name, url in processed_urls for date in dates]
    urls = [(name, url, address.replace(name + "',", '').replace('adress', 'индекс').replace("'", '')) for name, url in urls for address in addresses if name in address]
    print(f'Найдено {len(urls)} ссылок')
    return urls
