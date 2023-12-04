import time

from playwright.async_api._generated import Page

from .html_parser import html_parser
from datetime import datetime

from ..settings import settings


def create_json(data, link_data, config):
    lines = []
    for k, v in data.items():
        for d in v:
            json_dict = {"values": {}}
            d['Адрес'] = link_data.address
            d['Подраздел'] = k
            for number, key in config.bipium_keys.items():
                json_dict['values'][number] = d[key]
            lines.append(json_dict)
    return lines

def create_list(data, link_data, config):
    lines = []
    for k, v in data.items():
        for d in v:
            d['Адрес'] = link_data.address
            d['Подраздел'] = k
            d['Дата сборки'] = datetime.now().strftime('%d.%m.%Y')
            line = [d[key] for key in settings.CSV_TITLES]
            lines.append(line)
    return lines

def get_lines(data, link_data, config):
    writer = config.writer
    if writer == 'excel':
        return create_list(data, link_data, config)
    elif writer == 'bipium':
        return create_json(data, link_data, config)


async def check_case(page: Page):
    all_content = []
    page_content = await page.content()
    header_elements = await page.query_selector('tr.text-center')
    if not header_elements and 'наименование события' in page_content.lower():
        h_trs = await page.query_selector_all('tr')
        for tr in h_trs:
            tr_text = await tr.text_content()
            if 'наименование события' in tr_text.lower():
                header_elements = tr
                break
    headers = [await td.text_content() for td in await header_elements.query_selector_all('td')]
    trs = await page.query_selector_all('tr')
    for tr in trs:
        tr_text = await tr.text_content()
        if 'рассмотрение дела' in tr_text.lower() or 'судебное заседание' in tr_text.lower():
            content_element = [await td.text_content() for td in await tr.query_selector_all('td')]
            all_content.append(content_element)
    if len(all_content) > 1:
        return True
    elif all_content:
        content = dict(zip(headers, all_content[0]))
        key = [i for i in content.keys() if 'результат' in i.lower()]
        if not key:
            return False
        if content[key[0]].replace(' ', ''):
            return True

async def create_lines(page: Page, link_data, config):
    page_content = await page.content()
    data = html_parser(page_content, link_data, config)
    for d_type, lines in data.items():
        for line in lines:
            await page.goto(line['URL дела'])
            page_content = await page.content()
            if 'движение дела' in page_content.lower() and ('рассмотрение дела' in page_content.lower() or 'судебное заседание' in page_content.lower()):
                case = await check_case(page)
                if case:
                    line['Заседание'] = 'Было'
    lines = get_lines(data, link_data, config)
    return lines


async def write(page, link_data, config, writer):
    lines = await create_lines(page, link_data, config)
    r = await writer.write_lines(lines)

