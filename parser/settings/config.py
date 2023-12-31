import configparser
import json
from datetime import datetime, timedelta

from . import settings


class Config:

    def __init__(self):
        with open(fr'{settings.CONFIG_FILES_DIR}\templates.json', encoding='utf-8-sig') as templates:
            self.templates_config = json.load(templates)

        with open(fr'{settings.CONFIG_FILES_DIR}\exception_words.json', encoding='utf-8-sig') as words:
            self.except_words = json.load(words)

        with open(fr'{settings.CONFIG_FILES_DIR}\proxies.json', encoding='utf-8-sig') as proxies:
            self.proxies_json = json.load(proxies)

        with open(fr'{settings.CONFIG_FILES_DIR}\bipium_keys.json', encoding='utf-8-sig') as keys:
            self.bipium_field_keys = json.load(keys)

        self.main_config = configparser.ConfigParser()
        self.main_config.read(fr'{settings.CONFIG_FILES_DIR}\MainConfig.ini', encoding='utf-8-sig')

    @property
    def _template(self) -> dict:
        template_name = self.main_config.get('main_settings', 'template_name')
        return self.templates_config[template_name]

    @property
    def regions_and_cities(self) -> dict | None:
        regions = self._template['regions']
        if not regions:
            return None
        return regions

    @property
    def dates(self):
        days = [int(i.strip()) for i in self._template['days'].split(',')]
        dates = [(datetime.now() + timedelta(days=day)).strftime('%d.%m.%Y') for day in days]
        return dates

    @property
    def proxies(self):
        if not self.proxies_json:
            return ['']
        return self.proxies_json

    @property
    def browsers_and_pages(self):
        bp = {'browsers': self.main_config.getint('main_settings', 'browsers'),
              'pages': self.main_config.getint('main_settings', 'pages')}
        if (not bp['browsers'] or bp['browsers'] > len(self.proxies)) and self.proxies_json:
            bp['browsers'] = len(self.proxies)
        elif not bp['browsers'] and not self.proxies_json:
            bp['browsers'] = 1
        return bp

    @property
    def semaphore(self):
        semaphore = self.main_config.getint('main_settings', 'semaphore')
        if not self.proxies_json and not semaphore:
            semaphore = 1
        elif not semaphore:
            semaphore = len(self.proxies)
        return semaphore

    @property
    def capmonster_token(self):
        return self.main_config.get('data', 'capmonster_token')

    @property
    def processes(self):
        return self.main_config.getint('main_settings', 'processes')

    @property
    def headless(self):
        return self.main_config.getboolean('main_settings', 'headless')

    @property
    def bipium_catalog(self):
        return self.main_config.get('bipium', 'bipium_catalog')

    @property
    def bipium_domain(self):
        return self.main_config.get('bipium', 'bipium_domain')

    @property
    def bipium_login(self):
        return self.main_config.get('bipium', 'bipium_login')

    @property
    def bipium_password(self):
        return self.main_config.get('bipium', 'bipium_password')

    @property
    def bipium_keys(self):
        return dict(self.bipium_field_keys)

    @property
    def articles(self):
        return [i.strip() for i in self._template['articles'].split(',')]

    @property
    def writer(self):
        return self.main_config.get('main_settings', 'csv_or_bipium')

    @property
    def start_time(self):
        return [i.strip() for i in self.main_config.get('main_settings', 'start_time').split(',')]

    @property
    def check_dates(self):
        date_now = datetime.now().strftime('%d.%m.%Y')
        stop_dates = [i.strip() for i in self.main_config.get('main_settings', 'stop_dates').split(',')]
        return not date_now in stop_dates

    @property
    def start_now(self):
        start = self.main_config.getboolean('main_settings', 'start_now')
        if start:
            self.main_config.set('main_settings', 'start_now', 'off')
            with open(fr'{settings.CONFIG_FILES_DIR}\MainConfig.ini', 'w') as f:
                self.main_config.write(f)
        return start

    @property
    def exception_words(self):
        return self.except_words['words']
