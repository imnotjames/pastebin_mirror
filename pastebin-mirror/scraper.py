#!/usr/bin/env python3
from json import JSONDecodeError
import requests


class PastebinComScraper:
    def __init__(self):
        self.__RAW_URL__ = 'https://pastebin.com/raw/'
        self.__ITEM_URL__ = 'https://pastebin.com/api_scrape_item.php'
        self.__METADATA_URL__ = 'https://pastebin.com/api_scrape_item_meta.php'
        self.__LIST_URL__ = 'https://pastebin.com/api_scraping.php'
        self.__ERROR_TEXT__ = 'Error, we cannot find this paste.'

    def get_paste_content(self, key):
        result = requests.get(self.__RAW_URL__ + key)

        if not result.ok:
            return None

        return result.content

    def get_paste_metadata(self, key):
        paste = requests.get(self.__METADATA_URL__, params={'i': key})

        if not paste.ok:
            return None

        if paste.text == self.__ERROR_TEXT__:
            return None

        try:
            paste_json = paste.json()
        except JSONDecodeError:
            return None

        if len(paste_json) == 0:
            return None

        return paste_json[0]

    def get_recent_pastes(self, limit=250):
        paste_list = requests.get(self.__LIST_URL__, params={'limit': min(250, limit)})

        if not paste_list.ok:
            return []

        try:
            return paste_list.json()
        except JSONDecodeError:
            return []
