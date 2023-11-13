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