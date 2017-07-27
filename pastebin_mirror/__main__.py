from pastebin_mirror.scraper import PastebinComScraper
from pastebin_mirror.storage import SQLite3Storage
import time
import logging

__version__='0.0.1'

logger = logging.getLogger(__name__)


def scrape_recent_pastes(scraper, storage):
    while True:
        recent_pastes = scraper.get_recent_pastes()

        for paste in recent_pastes:
            key = paste['key']

            logger.info('Found paste %s created on %s', key, paste['date'])

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
                logger.info('Fetching paste content for %s', key)

                storage.save_paste_content(key, scraper.get_paste_content(key))

        time.sleep(1)


if __name__ == '__main__':
    from argparse import ArgumentParser
    import sys
    import os

    parser = ArgumentParser(description='Mirror publicly uploaded pastes from Pastebin.com')

    parser.add_argument('file', metavar='file', nargs=1, help='sqlite file to save to')

    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--verbose', '-v', default=0, action='count', dest='verbose', help='increase verbosity, multiple times to increase it more')

    arguments = parser.parse_args()

    if arguments.verbose == 1:
        logging.basicConfig(level=logging.WARNING)
    elif arguments.verbose == 2:
        logging.basicConfig(level=logging.INFO)
    elif arguments.verbose >= 3:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    pastebin_sqlite_database = arguments.file[0]

    if os.path.isdir(pastebin_sqlite_database):
        logger.error('sqlite database must be a file')
        sys.exit(1)

    scraper = PastebinComScraper()
    storage = SQLite3Storage(pastebin_sqlite_database)

    storage.initialize_tables()

    scrape_recent_pastes(scraper, storage)
