import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from math import ceil

from ..settings import settings




def get_regions_value():
    ua = UserAgent()
    url = settings.ALL_REGIONS_URL
    headers = {'user-agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    regions_list = soup.find(id='ms_subj').find_all('option')[1:]
    regions_dict = {i.text: i['value'] for i in regions_list if all(reg not in i.text for reg in settings.NOT_PARSING)}
    return regions_dict


def region_decoder(region):
    return settings.REGION_VALUE_DECODE[region]


def city_decoder(city):
    city_code = ''
    symbols = settings.SYMBOLS_CITY_DECODE
    for char in city:
        city_code += symbols[char]

    return city_code


def split_list(lst, num_chunks):
    if num_chunks <= 0:
        return [lst]

    chunk_size = ceil(len(lst) / num_chunks)
    chunks = [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

    return chunks

def get_addresses():
    cookies = {
        'PHPSESSID': '0pjm2l5r96qcob90oede324k93',
    }

    headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=0pjm2l5r96qcob90oede324k93',
        'Referer': 'https://sudrf.ru/index.php?id=300&act=go_ms_search&searchtype=ms&var=true&ms_type=ms&court_subj=87',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.686 YaBrowser/23.9.5.686 Yowser/2.5 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'id': '300',
        'act': 'ya_coords',
        'type_suds': 'mir',
        '_': '1700937385479',
    }

    response = requests.get('https://sudrf.ru/index.php?id=300&act=ya_coords&type_suds=mir&_=1700937938198',
                            params=params, cookies=cookies, headers=headers)
    return [i.split("{type:'mir',name:'")[1].split("',coord:")[0] for i in response.text.split('= new Array();')[1:]]