import requests
import logging
import re
from json import JSONDecodeError
from lxml import html

logger = logging.getLogger(__name__)


class PastebinComScraper:
    def __init__(self):
        self.__RAW_URL__ = 'https://pastebin.com/raw/'
        self.__ITEM_URL__ = 'https://scrape.pastebin.com/api_scrape_item.php'
        self.__METADATA_URL__ = 'https://scrape.pastebin.com/api_scrape_item_meta.php'
        self.__LIST_URL__ = 'https://scrape.pastebin.com/api_scraping.php'
        self.__ARCHIVE_URL__ = 'https://pastebin.com/archive'
        self.__ERROR_TEXT__ = 'Error, we cannot find this paste.'
        self.__NOT_WHITELISTED_MATCHER__ = re.compile('^THIS IP: [^ ]+ DOES NOT HAVE ACCESS. VISIT: https://pastebin.com/scraping TO GET ACCESS!$')

        self.use_fallback_listing = False

    def get_paste_content(self, key):
        result = requests.get(self.__RAW_URL__ + key)

        if not result.ok:
            logger.error('http status not OK: code %d', result.status_code)
            return None

        return result.content

    def get_paste_metadata(self, key):
        paste = requests.get(self.__METADATA_URL__, params={'i': key})

        logger.debug('made request to %s for paste %s', self.__METADATA_URL__, key)

        if not paste.ok:
            logger.error('http status not OK: code %d', paste.status_code)
            return None

        if paste.text == self.__ERROR_TEXT__ :
            logger.error('cannot find paste')
            return None

        try:
            paste_json = paste.json()
        except JSONDecodeError:
            logger.error('response not json: %s', paste.text)
            return None

        if len(paste_json) == 0:
            logger.error('cannot find paste')
            return None

        return paste_json[0]

    def _get_recent_pastes_fallback(self, limit=250):
        logger.debug('retrieving at most %d recent pastes using fallback', limit)

        response = requests.get(self.__ARCHIVE_URL__)

        if not response.ok:
            logger.error('http status not OK: code %d', response.status_code)
            return []

        paste_list_tree = html.fromstring(response.content)

        paste_list = paste_list_tree.xpath('//div[@id=\'content_left\']//table[@class=\'maintable\']//td[1]//a/@href')

        return [self.get_paste_metadata(str(key).lstrip('/')) for key in paste_list[:limit]]

    def get_recent_pastes(self, limit=250):
        limit = min(250, limit)

        if self.use_fallback_listing:
            return self._get_recent_pastes_fallback(limit)

        logger.debug('retrieving at most %d recent pastes', limit)

        paste_list = requests.get(self.__LIST_URL__, params={'limit': limit})

        if not paste_list.ok:
            logger.error('http status not OK: code %d', paste_list.status_code)
            return []

        try:
            return paste_list.json()
        except JSONDecodeError:
            if self.__NOT_WHITELISTED_MATCHER__.match(paste_list.text):
                logger.error('your IP address is not whitelisted, it must be to get recent pastes')

                self.use_fallback_listing = True

                return self._get_recent_pastes_fallback()
            else:
                logger.error('response not json: %s', paste_list.text)

            return []
