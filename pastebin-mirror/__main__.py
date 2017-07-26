from scraper import PastebinComScraper
from storage import SQLite3Storage
import time
import sys
import os


def usage():
    print("pastebin-mirror [sqlite-file]")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    pastebin_sqlite_database = sys.argv[1]

    if os.path.isdir(pastebin_sqlite_database):
        usage()
        sys.exit(1)

    scraper = PastebinComScraper()
    storage = SQLite3Storage()

    storage.initialize_tables()

    while True:
        recent_pastes = scraper.get_recent_pastes()

        for paste in recent_pastes:
            key = paste['key']

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
                print("Fetching paste content for %s" % key)

                storage.save_paste_content(key, scraper.get_paste_content(key))

        time.sleep(1)
