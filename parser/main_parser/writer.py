import time

from playwright.async_api._generated import Page

from .html_parser import html_parser
from datetime import datetime

from ..settings import settings


def create_json(data, link_data, config):
    print(1, 'json')
    lines = []
    for k, v in data.items():
        print(2, 'json')
        for d in v:
            print(3, 'json')
            json_dict = {"values": {}}
            print(4, 'json')
            d['Адрес'] = link_data.address
            print(5, 'json')
            d['Подраздел'] = k
            print(6, 'json')
            print(config.bipium_keys.items())
            for number, key in config.bipium_keys.items():
                print(7, 'json')
                json_dict['values'][number] = d[key]
                print(8, 'json')
            lines.append(json_dict)
            print(9, 'json')
    print(10, 'json')
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
    print(1, 'lones')
    writer = config.writer
    print(2, 'lones')
    if writer == 'excel':
        print(2.1, 'lones')
        return create_list(data, link_data, config)
    elif writer == 'bipium':
        print(2.2, 'lones')
        return create_json(data, link_data, config)


async def check_case(page: Page):
    all_content = []
    header_elements = await page.query_selector('tr.text-center')
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
        [key] = [i for i in content.keys() if 'результат' in i.lower()]
        if content[key].replace(' ', ''):
            return True

async def create_lines(page: Page, link_data, config):
    print(1)
    page_content = await page.content()
    data = html_parser(page_content, link_data, config)
    for d_type, lines in data.items():
        for line in lines:
            print(line)
            await page.goto(line['URL дела'])
            print(2)
            page_content = await page.content()
            print(3)
            if 'движение дела' in page_content.lower() and ('рассмотрение дела' in page_content.lower() or 'судебное заседание' in page_content.lower()):
                print(4)
                case = await check_case(page)
                print(5)
                if case:
                    print(5.5)
                    line['Заседание'] = 'Было'
                print(6)
    print(7)
    lines = get_lines(data, link_data, config)
    print(8)
    return lines


async def write(page, link_data, config, writer):
    lines = await create_lines(page, link_data, config)
    r = await writer.write_lines(lines)
    print(r)

