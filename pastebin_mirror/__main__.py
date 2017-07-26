from scraper import PastebinComScraper
from storage import SQLite3Storage
import time
import sys
import os
import logging

logger = logging.getLogger(__name__)


def scrape_recent_pastes(scraper, storage):
    while True:
        recent_pastes = scraper.get_recent_pastes()

        for paste in recent_pastes:
            key = paste['key']

            logger.info('Found paste %(key)s created %(created)s', extra={'paste': key, 'created': paste['date']})

            storage.save_paste_reference(
                key,
                paste['size'],
                paste['date'],
                paste['expire'],
                paste['title'],
                paste['syntax'],
                paste['user']
            )

            if not storage.has_paste_content(key):
                logger.info('Fetching paste content for %(key)s', extra={'paste': key})

                storage.save_paste_content(key, scraper.get_paste_content(key))

        time.sleep(1)


if __name__ == '__main__':
    arguments = sys.argv

    arguments.pop(0)

    if '-v' in arguments:
        logging.basicConfig(level=logging.INFO)

    if len(arguments) < 2:
        print("[-v] [sqlite-file]")
        sys.exit(1)

    pastebin_sqlite_database = arguments[0]

    if os.path.isdir(pastebin_sqlite_database):
        logger.error('sqlite database must be a file')
        sys.exit(1)

    scraper = PastebinComScraper()
    storage = SQLite3Storage(pastebin_sqlite_database)

    storage.initialize_tables()

    scrape_recent_pastes(scraper, storage)
