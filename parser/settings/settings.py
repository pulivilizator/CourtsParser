import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

REGIONS_URL = 'https://sudrf.ru/index.php?id=300&var=true'
ALL_REGIONS_URL = 'https://sudrf.ru/index.php?id=300&act=go_ms_search&searchtype=ms&var=true&ms_type=ms&court_subj=0'
FORMAT_REGIONS_URL = 'https://sudrf.ru/index.php?id=300&act=go_ms_search&searchtype=ms&var=true&ms_type=ms&court_subj={}&ms_city={}&ms_street='
CONFIG_FILES_DIR = os.path.join(BASE_DIR, r'config_files')

NOT_PARSING = ['Татарстан', 'Оренбургская область', 'Москва', 'Санкт-Петербург', 'Севастополь', 'Красноярский', 'Город', 'Югра', 'Чеченская', 'Ставропольский', 'Мордовия', 'Псковская', 'Крым', 'Межрегиональные']
NOT_PARSING_URLS = ['tatar', 'kodms.ru', 'mos-sud.ru/ms', 'mirsud.spb.ru', 'mirsud.sev.gov.ru/', 'mirsud24.ru/reference/su', 'mirsud86.ru/', 'mirsud-chr.ru', 'stavmirsud.ru', 'mirsud.e-mordovia.ru', 'mirsud.pskov.ru', 'mirsud82.rk.gov.ru']

SYMBOLS_CITY_DECODE = {'А': '%C0', 'а': '%E0', 'Б': '%C1', 'б': '%E1', 'В': '%C2', 'в': '%E2', 'Г': '%C3', 'г': '%E3',
                  'Д': '%C4', 'д': '%E4', 'Е': '%C5', 'е': '%E5', 'Ё': '%A8', 'ё': '%B8', 'Ж': '%C6', 'ж': '%E6',
                  'З': '%C7', 'з': '%E7', 'И': '%C8', 'и': '%E8', 'Й': '%C9', 'й': '%E9', 'К': '%CA', 'к': '%EA',
                  'Л': '%CB', 'л': '%EB', 'М': '%CC', 'м': '%EC', 'Н': '%CD', 'н': '%ED', 'О': '%CE', 'о': '%EE',
                  'П': '%CF', 'п': '%EF', 'Р': '%D0', 'р': '%F0', 'С': '%D1', 'с': '%F1', 'Т': '%D2', 'т': '%F2',
                  'У': '%D3', 'у': '%F3', 'Ф': '%D4', 'ф': '%F4', 'Х': '%D5', 'х': '%F5', 'Ц': '%D6', 'ц': '%F6',
                  'Ч': '%D7', 'ч': '%F7', 'Ш': '%D8', 'ш': '%F8', 'Щ': '%D9', 'щ': '%F9', 'Ъ': '%DA', 'ъ': '%FA',
                  'Ы': '%DB', 'ы': '%FB', 'Ь': '%DC', 'ь': '%FC', 'Э': '%DD', 'э': '%FD', 'Ю': '%DE', 'ю': '%FE',
                  'Я': '%DF', 'я': '%FF'}

REGION_VALUE_DECODE = {'Алтайский край': '22', 'Амурская область': '28', 'Архангельская область': '29',
                       'Астраханская область': '30', 'Белгородская область': '31', 'Брянская область': '32',
                       'Владимирская область': '33', 'Волгоградская область': '34', 'Вологодская область': '35',
                       'Воронежская область': '36', 'Еврейская автономная область': '79', 'Забайкальский край': '75',
                       'Ивановская область': '37', 'Иркутская область': '38', 'Кабардино-Балкарская Республика': '07',
                       'Калининградская область': '39', 'Калужская область': '40', 'Камчатский край': '41',
                       'Карачаево-Черкесская Республика': '09', 'Кемеровская область - Кузбасс': '42',
                       'Кировская область': '43', 'Костромская область': '44', 'Краснодарский край': '23',
                       'Курганская область': '45', 'Курская область': '46', 'Ленинградская область': '47',
                       'Липецкая область': '48', 'Магаданская область': '49', 'Московская область': '50',
                       'Мурманская область': '51', 'Ненецкий автономный округ': '83', 'Нижегородская область': '52',
                       'Новгородская область': '53', 'Новосибирская область': '54', 'Омская область': '55',
                       'Орловская область': '57', 'Пензенская область': '58', 'Пермский край': '59',
                       'Приморский край': '25', 'Республика Адыгея': '01', 'Республика Алтай': '02',
                       'Республика Башкортостан': '03', 'Республика Бурятия': '04', 'Республика Дагестан': '05',
                       'Республика Ингушетия': '06', 'Республика Калмыкия': '08', 'Республика Карелия': '10',
                       'Республика Коми': '11', 'Республика Марий Эл': '12', 'Республика Саха (Якутия)': '14',
                       'Республика Северная Осетия-Алания': '15', 'Республика Тыва': '17', 'Республика Хакасия': '19',
                       'Ростовская область': '61', 'Рязанская область': '62', 'Самарская область': '63',
                       'Саратовская область': '64', 'Сахалинская область': '65', 'Свердловская область': '66',
                       'Смоленская область': '67', 'Тамбовская область': '68', 'Тверская область': '69',
                       'Томская область': '70', 'Тульская область': '71', 'Тюменская область': '72',
                       'Удмуртская Республика': '18', 'Ульяновская область': '73', 'Хабаровский край': '27',
                       'Челябинская область': '74', 'Чувашская Республика - Чувашия': '21',
                       'Чукотский автономный округ': '87', 'Ямало-Ненецкий автономный округ': '89', 'Ярославская область': '76'}

CODES = ['АПК', 'ВК', 'ГК', 'ГПК', 'ЖК', 'ЗК', 'КАС', 'КоАП', 'СК', 'ТК', 'УИК', 'УПК', 'УК']

REGIONS_URL_CODES = {'alt': 'Алтайский край', 'amr': 'Амурская область', 'arh': 'Ненецкий автономный округ',
                     'ast': 'Астраханская область', 'blg': 'Белгородская область', 'brj': 'Брянская область',
                     'wld': 'Владимирская область', 'vol': 'Волгоградская область', 'vld': 'Вологодская область',
                     'vrn': 'Воронежская область', 'eao': 'Еврейская автономная область', 'zbk': 'Забайкальский край',
                     'iwn': 'Ивановская область', 'irk': 'Иркутская область', 'kbr': 'Кабардино-Балкарская Республика',
                     'kln': 'Калининградская область', 'klg': 'Калужская область', 'kmch': 'Камчатский край',
                     'kchr': 'Карачаево-Черкесская Республика', 'kmr': 'Кемеровская область - Кузбасс', 'kir': 'Кировская область',
                     'kst': 'Костромская область', 'krd': 'Краснодарский край', 'krg': 'Курганская область',
                     'krs': 'Курская область', 'lo': 'Ленинградская область', 'lipetsk': 'Липецкая область',
                     'mag': 'Магаданская область', 'mo': 'Московская область', 'mrm': 'Мурманская область',
                     'nnov': 'Нижегородская область', 'nvg': 'Новгородская область', 'nsk': 'Новосибирская область',
                     'oms': 'Омская область', 'orl': 'Орловская область', 'pnz': 'Пензенская область', 'perm': 'Пермский край',
                     'prm': 'Приморский край', 'adg': 'Республика Адыгея', 'ralt': 'Республика Алтай', 'bkr': 'Республика Башкортостан',
                     'bur': 'Республика Бурятия', 'dag': 'Республика Дагестан', 'ing': 'Республика Ингушетия',
                     'kalm': 'Республика Калмыкия', 'kar': 'Республика Карелия', 'komi': 'Республика Коми', 'mari': 'Республика Марий Эл',
                     'yak': 'Республика Саха (Якутия)', 'rso': 'Республика Северная Осетия-Алания', 'tuva': 'Республика Тыва',
                     'hak': 'Республика Хакасия', 'ros': 'Ростовская область', 'riz': 'Рязанская область', 'sam': 'Самарская область',
                     'sar': 'Саратовская область', 'sah': 'Сахалинская область', 'svd': 'Свердловская область', 'sml': 'Смоленская область',
                     'tmb': 'Тамбовская область', 'twr': 'Тверская область', 'tms': 'Томская область', 'tula': 'Тульская область',
                     'tyum': 'Тюменская область', 'udm': 'Удмуртская Республика', 'uln': 'Ульяновская область', 'hbr': 'Хабаровский край',
                     'chel': 'Челябинская область', 'chv': 'Чувашская Республика - Чувашия', 'chao': 'Чукотский автономный округ',
                     'ynao': 'Ямало-Ненецкий автономный округ', 'jrs': 'Ярославская область'}