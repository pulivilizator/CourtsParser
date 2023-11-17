from bs4 import BeautifulSoup
from datetime import datetime, date
from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc,
    AddrExtractor,
    LOC,
)

from ..settings import settings


def created_html_dict(soup):
    td_elements = soup.find_all('td')
    html_page_dict = {}
    for html_title in td_elements:
        if html_title.has_attr('colspan'):
            title = html_title.text
            html_page_dict[title] = []
    return html_page_dict


def html_parser(page_content, link_data, config):
    soup = BeautifulSoup(page_content, 'html.parser')
    title = None
    html_page_dict = created_html_dict(soup)
    tr_elements = soup.find(id='tablcont').find_all('tr')
    column_list = [i.text for i in tr_elements[0].find_all('td')]
    for tr in tr_elements[1:]:
        tmp_key = tr.text
        if tmp_key in html_page_dict:
            title = tmp_key
            continue
        tmp_dict = create_tmp_dict(link_data, tr, column_list, config)
        if tmp_dict is None:
            continue
        html_page_dict[title].append(tmp_dict)

    return html_page_dict

def create_tmp_dict(link_data, tr, column_list, config):
    url = link_data.url
    success_articles = config.articles
    court_name = link_data.court_name
    # print('tmp start', url)
    tmp_dict = {'Номер дела': '-', 'Время слушания': '-', 'Событие': '-', 'Информация по делу': '-', 'Результат слушания': '', 'Судья': '-'}
#     print(1, url)
    td_elements = tr.find_all('td')
#     print(2, url)
    for column, td in zip(column_list, td_elements):
        tmp_dict[column] = td.text
    tmp_dict['Информация по делу'] = tmp_dict['Информация по делу'].replace('  ', ' ')
#     print(3, url)
    article, codes = get_article_codes(tmp_dict['Информация по делу'])
    if article not in success_articles and success_articles[0] != 'all':
        return None
    tmp_dict['Номер статьи'] = article.replace(';', '')
#     print(3.5)
    td_href = tr.find('a')
    if td_href.has_attr('href'):
        tmp_dict['URL дела'] = url.split('.ru')[0] + '.ru' + td_href['href']
    else:
        tmp_dict['URL дела'] = url
#     print(4, url)
#     print(5, url)
    tmp_dict['Участок'] = court_name
#     print(6, url)
    tmp_dict['Город'] = get_city(court_name)
#     print(7, url)
    tmp_dict['URL страницы'] = url
#     print(8, url)
    date = datetime.strptime(url[-10:], '%d.%m.%Y')
#     print(9, url)
    tmp_dict['Дата'] = date.strftime('%Y-%m-%d')
#     print(10, url)
    tmp_dict['Кодекс'] = codes
#     print(12, url)
    # tmp_dict['Дата сборки'] = datetime.now().strftime("%d.%m.%Y")
    tmp_dict['Количеством дней'] = str(get_days(tmp_dict['Дата']))
#     print(13, url)
    tmp_dict['Регион'] = get_region(url)
#     print(14, url)
    fio_dict = get_fio(tmp_dict['Информация по делу'])
#     print(15, url)
    if fio_dict:
#         print(16, url)
        fio = list(fio_dict.keys())[0]
#         print(17, url)
        fio_sep = fio_dict[fio]
#         print(18, url)
        tmp_dict['ФИО'] = fio
#         print(19, url)
        tmp_dict['Фамилия Имя'] = fio_sep['last'] + ' ' + fio_sep['first']
#         print(20, url)
        tmp_dict['Имя Отчество'] = fio_sep['first'] + ' ' + fio_sep['middle']
#         print(21, url)
        tmp_dict['Фамилия'] = fio_sep['last']
#         print(22, url)
        tmp_dict['Имя'] = fio_sep['first']
#         print(23, url)
        tmp_dict['Отчество'] = fio_sep['middle']
#         print(24, url)
        tmp_dict['ФИО и номер дела'] = tmp_dict['ФИО'] + ' ' + tmp_dict['Номер дела']
#         print(25, url)
        tmp_dict['ФИО и дата дела'] = tmp_dict['ФИО'] + ' ' + date.strftime('%d.%m.%Y')
#         print(26, url)
        tmp_dict['ФИО и область'] = tmp_dict['ФИО'] + ' ' + get_region(url)
#         print(27, url)
    else:
        tmp_dict['ФИО'] = '-'
        tmp_dict['Фамилия Имя'] = '-'
        tmp_dict['Имя Отчество'] = '-'
        tmp_dict['Фамилия'] = '-'
        tmp_dict['Имя'] = '-'
        tmp_dict['Отчество'] = '-'
        tmp_dict['ФИО и номер дела'] = '-'
        tmp_dict['ФИО и дата дела'] = '-'
        tmp_dict['ФИО и область'] = '-'
    # print('tmp end')
    return tmp_dict



def get_city(court_name: str):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    addr_extractor = AddrExtractor(morph_vocab)

    matches = addr_extractor(court_name)
    facts = [i.fact.as_json for i in matches]

    for i in facts:
        if 'type' in i.keys() and i['type'] == 'город':
            return i['value']
    return '-'

def get_article_codes(info):
    codes = '-'
    if 'ст.' in info:
        info = info.split('ст.')[1].strip(';').split('(')
    elif '- ' in info:
        info = info.split('- ')[-1].strip(';').split('(')
    else:
        return ('-', '-')
    article = info[0].replace(' ', '')
    if len(info) > 1:
        codes = info[1].split(')')[0]
    if not article[0].isdigit() or article[1] in ['\'', '"']:
        article = codes = '-'
    return (article, codes)

# def get_codes(info):
#     info = info.replace('ООО УК', '').replace('АО УК', '')
#     codes = ''
#     for c in settings.CODES:
#         if f'({c})' in info or f' {c} ' in info:
#             codes += f' {c}'
#     if codes:
#         return codes.strip()
#     return '-'

def get_fio(text):
    text = 'Истец: ' + text.replace('ОТВЕТЧИК', ' ').title()
    emb = NewsEmbedding()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        span.normalize(morph_vocab)

    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)

    fio_dict = {_.normal.title(): _.fact.as_dict for _ in doc.spans if _.fact}
    for k, v in fio_dict.items():
        fio = k.split()
        if len(fio) == 3:
            return {' '.join(fio).title(): {'first': fio[1].title(), 'last': fio[0].title(), 'middle': fio[2].title()}}
    fio = list(fio_dict.keys())
    if len(fio) == 1 and len(fio[0].split()) == 3:
        fio = fio[0].split()
        return {' '.join(fio).title(): {'first': fio[1].title(), 'last': fio[0].title(), 'middle': fio[2].title()}}
    elif len(fio) == 2 and len(fio[0].split()) + len(fio[1].split()) == 3:
        fio = ' '.join(fio[:2]).split()
        return {' '.join(fio).title(): {'first': fio[1].title(), 'last': fio[0].title(), 'middle': fio[2].title()}}
    elif len(fio) == 3 and len(fio[0].split()) + len(fio[1].split()) + len(fio[2].split()) == 3:
        fio = ' '.join(fio[:3]).split()
        return {' '.join(fio).title(): {'first': fio[1].title(), 'last': fio[0].title(), 'middle': fio[2].title()}}

def get_region(url):
    return settings.REGIONS_URL_CODES[url.split('.')[1]]

def get_days(dates):
    date_now = date.fromisoformat(datetime.now().strftime("%Y-%m-%d"))
    dates = date.fromisoformat(dates)

    difference = dates - date_now
    difference_in_days = difference.days
    return difference_in_days

def create_json(page_content, link_data, config):
    data = html_parser(page_content, link_data, config)
    lines = []
    for k, v in data.items():
        for d in v:
            json_dict = {"values": {}}
            d['Подраздел'] = k
            for number, key in config.bipium_keys.items():
                json_dict['values'][number] = d[key]
            lines.append(json_dict)
    return lines

def create_list(page_content, link_data, config):
    lines = []
    data = html_parser(page_content, link_data, config)
    for k, v in data.items():
        for d in v:
            d['Подраздел'] = k
            d['Дата сборки'] = datetime.now().strftime('%d.%m.%Y')
            line = [d[key] for key in settings.CSV_TITLES]
            lines.append(line)
    return lines

def get_lines(page_content, link_data, config):
    writer = config.writer
    if writer == 'excel':
        return create_list(page_content, link_data, config)
    elif writer == 'bipium':
        return create_json(page_content, link_data, config)