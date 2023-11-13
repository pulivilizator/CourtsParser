from pprint import pp

from .courts import get_processing_urls


async def create_urls(config):
    processed_urls = await get_processing_urls(config)
    dates = config.dates
    urls = [url + '/modules.php?name=sud_delo&op=hl&H_date=' + date
            if url[-1] != '/'
            else url[:-1] + '/modules.php?name=sud_delo&op=hl&H_date=' + date
            for url in processed_urls for date in dates]
    print(f'Найдено {len(urls)} ссылок')
    return urls
