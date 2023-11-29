from bs4 import BeautifulSoup
from datetime import datetime, date

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
    tmp_dict = {'Номер дела': '-', 'Время слушания': '-', 'Событие': '-', 'Информация по делу': '-', 'Результат слушания': '', 'Судья': '-', 'Заседание': 'Не было'}
    td_elements = tr.find_all('td')
    for column, td in zip(column_list, td_elements):
        tmp_dict[column] = td.text
    tmp_dict['Информация по делу'] = tmp_dict['Информация по делу'].replace('  ', ' ')
    article, codes = get_article_codes(tmp_dict['Информация по делу'])
    if article not in success_articles and success_articles[0] != 'all':
        return None
    tmp_dict['Номер статьи'] = article.replace(';', '')
    td_href = tr.find('a')
    if td_href.has_attr('href'):
        tmp_dict['URL дела'] = url.split('.ru')[0] + '.ru' + td_href['href']
    else:
        tmp_dict['URL дела'] = url
    tmp_dict['Участок'] = court_name
    tmp_dict['Город'] = get_city(link_data.address)
    tmp_dict['URL страницы'] = url
    date = datetime.strptime(url[-10:], '%d.%m.%Y')
    tmp_dict['Дата'] = date.strftime('%Y-%m-%d')
    tmp_dict['Кодекс'] = codes
    tmp_dict['Количеством дней'] = str(get_days(tmp_dict['Дата']))
    tmp_dict['Регион'] = get_region(url)
    fio_dict = get_fio(tmp_dict['Информация по делу'], config)
    if fio_dict:
        fio = list(fio_dict.keys())[0]
        fio_sep = fio_dict[fio]
        tmp_dict['ФИО'] = fio
        tmp_dict['Фамилия Имя'] = fio_sep['last'] + ' ' + fio_sep['first']
        tmp_dict['Имя Отчество'] = fio_sep['first'] + ' ' + fio_sep['middle']
        tmp_dict['Фамилия'] = fio_sep['last']
        tmp_dict['Имя'] = fio_sep['first']
        tmp_dict['Отчество'] = fio_sep['middle']
        tmp_dict['ФИО и номер дела'] = tmp_dict['ФИО'] + ' ' + tmp_dict['Номер дела']
        tmp_dict['ФИО и дата дела'] = tmp_dict['ФИО'] + ' ' + date.strftime('%d.%m.%Y')
        tmp_dict['ФИО и область'] = tmp_dict['ФИО'] + ' ' + get_region(url)

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
    return tmp_dict



def get_city(court_name: str):###
    if ' г.' in court_name:
        return court_name.split(' г.')[1].strip().split(',')[0]
    elif ' городе' in court_name:
        return court_name.split(' городе')[1].strip().split(',')[0]
    elif ' города' in court_name:
        return court_name.split(' города')[1].strip().split(',')[0]
    elif ' с.' in court_name:
        return court_name.split(' с.')[1].strip().split(',')[0]
    elif ' п.' in court_name:
        return court_name.split(' п.')[1].strip().split(',')[0]
    elif ' пгт ' in court_name or ' пгт.' in court_name:
        return court_name.split(' пгт')[1].strip().strip('.').split(',')[0]
    elif ' рп.' in court_name:
        return court_name.split(' рп.')[1].strip().split(',')[0]
    elif ' х.' in court_name:
        return court_name.split(' х.')[1].strip().split(',')[0]
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
    if not article[0].isdigit() or (len(article) > 1 and article[1] in ['\'', '"']):
        article = codes = '-'

    return (article, codes)

def get_fio(text, config):
    results = []
    text = text.split(' - ')[0]
    for w in settings.REPL_WORDS:
        text = text.replace(w, '')
        text = text.replace(w.title(), '')
        text = text.replace(w.lower(), '')

    def get_lst(sep, text):
        lst = []
        vars = [i for i in text.split(sep)
                if len(i.strip().split()) == 3 and not any(f.upper() in i or f.title() in i.title() for f in config.exception_words)]
        for fio in vars:
            if not fio: continue
            fio = fio.strip().strip(';').strip(':').strip('"')
            if len(fio.split()) == 3 and '"' not in fio and all(len(i) > 2 for i in fio.split()):
                fio = fio.split()
                lst.append({' '.join(fio).title(): {'first': fio[1].title(), 'last': fio[0].title(),
                                                    'middle': fio[2].title()}})
        if lst:
            return lst
        else:
            for i in text.split(sep):
                if i:
                    vars = [k for k in i.split(',')
                            if len(k.strip().split()) == 3 and not any(f.lower() in k.lower() for f in config.exception_words)]
                    for fio in vars:
                        if not fio: continue
                        fio = fio.strip().strip(';').strip(':').strip('"')
                        if len(fio.split()) == 3 and '"' not in fio and all(len(i) > 2 for i in fio.split()):
                            fio = fio.split()
                            lst.append({' '.join(fio).title(): {'first': fio[1].title(), 'last': fio[0].title(),
                                                                'middle': fio[2].title()}})
            return lst
    results.extend(get_lst(':', text))
    results.extend(get_lst('" ', text))
    if results:
        return results[0]
    return None


def get_region(url):
    return settings.REGIONS_URL_CODES[url.split('.')[1]]

def get_days(dates):
    date_now = date.fromisoformat(datetime.now().strftime("%Y-%m-%d"))
    dates = date.fromisoformat(dates)

    difference = dates - date_now
    difference_in_days = difference.days
    return difference_in_days
