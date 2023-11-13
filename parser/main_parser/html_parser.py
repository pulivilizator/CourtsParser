from bs4 import BeautifulSoup
from datetime import datetime, date
from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc
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


def html_parser(page_content, url):
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
        tmp_dict = create_tmp_dict(soup, url, tr, column_list)
        html_page_dict[title].append(tmp_dict)

    return html_page_dict

def create_tmp_dict(soup, url, tr, column_list):
    print('tmp start', url)
    tmp_dict = {'Номер дела': '-', 'Время слушания': '-', 'Событие': '-', 'Информация по делу': '-', 'Результат слушания': '', 'Судья': '-'}
    print(1, url)
    td_elements = tr.find_all('td')
    print(2, url)
    for column, td in zip(column_list, td_elements):
        tmp_dict[column] = td.text
    print(3, url)
    tmp_dict['Номер статьи'] = get_article(tmp_dict['Информация по делу']).replace(';', '')
    print(3.5)
    td_href = tr.find('a')
    if td_href.has_attr('href'):
        tmp_dict['URL дела'] = url.split('.ru')[0] + '.ru' + td_href['href']
    else:
        print(url, 13333411233966)
        tmp_dict['URL дела'] = url
    print(4, url)
    court_name = soup.find(id='court_name').text
    print(5, url)
    tmp_dict['Участок'] = court_name
    print(6, url)
    tmp_dict['Город'] = get_city(court_name)
    print(7, url)
    tmp_dict['URL страницы'] = url
    print(8, url)
    date = datetime.strptime(url[-10:], '%d.%m.%Y')
    print(9, url)
    tmp_dict['Дата'] = date.strftime('%Y-%m-%d')
    print(10, url)
    tmp_dict['Кодекс'] = get_codes(tmp_dict['Информация по делу'])
    print(12, url)
    # tmp_dict['Дата сборки'] = datetime.now().strftime("%d.%m.%Y")
    tmp_dict['Количеcтвом дней'] = str(get_days(tmp_dict['Дата']))
    print(13, url)
    tmp_dict['Регион'] = get_region(url)
    print(14, url)
    fio_dict = get_fio(tmp_dict['Информация по делу'])
    print(15, url)
    if fio_dict:
        print(16, url)
        fio = list(fio_dict.keys())[0]
        print(17, url)
        fio_sep = fio_dict[fio]
        print(18, url)
        tmp_dict['ФИО'] = fio
        print(19, url)
        tmp_dict['Фамилия Имя'] = fio_sep['last'] + ' ' + fio_sep['first']
        print(20, url)
        tmp_dict['Имя Отчество'] = fio_sep['first'] + ' ' + fio_sep['middle']
        print(21, url)
        tmp_dict['Фамилия'] = fio_sep['last']
        print(22, url)
        tmp_dict['Имя'] = fio_sep['first']
        print(23, url)
        tmp_dict['Отчество'] = fio_sep['middle']
        print(24, url)
        tmp_dict['ФИО и номер дела'] = tmp_dict['ФИО'] + ' ' + tmp_dict['Номер дела']
        print(25, url)
        tmp_dict['ФИО и дата дела'] = tmp_dict['ФИО'] + ' ' + date.strftime('%d.%m.%Y')
        print(26, url)
        tmp_dict['ФИО и область'] = tmp_dict['ФИО'] + ' ' + get_region(url)
        print(27, url)
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
    print('tmp end')
    return tmp_dict



def get_city(court_name: str):
    if 'г.' in court_name:
        return court_name.split('г.')[1].strip()
    elif 'города ' in court_name:
        return court_name.split('города ')[1]
    return '-'

def get_article(info):
    if 'ст.' in info:
        info = info.split('ст.')[1].strip(';')
    elif '- ' in info:
        info = info.split('- ')[-1].strip(';')
    else:
        return '-'
    info = info.split('(')[0].replace(' ', '')
    if not info[0].isdigit():
        info = '-'
    return info

def get_codes(info):
    codes = ''
    for c in settings.CODES:
        if f'({c})' in info or f' {c} ' in info:
            codes += f' {c}'
    if codes:
        return codes.strip()
    return '-'

def get_fio(text):
    text = text.replace('ОТВЕТЧИК', ' ')
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
        if len(v) == 3:
            return {k: v}

def get_region(url):
    return settings.REGIONS_URL_CODES[url.split('.')[1]]

def get_days(dates):
    date_now = date.fromisoformat(datetime.now().strftime("%Y-%m-%d"))
    dates = date.fromisoformat(dates)

    difference = dates - date_now
    difference_in_days = difference.days
    return difference_in_days

def create_json(page_content, url, config):
    print(url)
    data = html_parser(page_content, url)
    lines = []
    for k, v in data.items():
        for d in v:
            json_dict = {"values": {}}
            d['Подраздел'] = k
            for number, key in config.bipium_keys.items():
                json_dict['values'][number] = d[key]
            lines.append(json_dict)
    return lines