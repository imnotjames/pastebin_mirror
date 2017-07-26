import sqlite3
import logging

logger = logging.getLogger(__name__)


class SQLite3Storage:
    def __init__(self, location='pastebin.db'):
        self.connection = sqlite3.connect(location)

    def initialize_tables(self):
        logger.info('creating table `paste` if it doesn\'t exist')

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS paste (
                paste_key CHAR(8) PRIMARY KEY,
                timestamp TIMESTAMP,
                size INT,
                expires TIMESTAMP,
                title TEXT,
                syntax TEXT,
                user TEXT NULL
            );
            '''
        )

        logger.info('creating table `paste_content` if it doesn\'t exist')

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS paste_content (
                paste_key CHAR(8) PRIMARY KEY,
                raw_content TEXT
            );
            '''
        )

    def has_paste_content(self, key):
        cursor = self.connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM paste_content WHERE paste_key = ?', (key,))

        paste_content_count = cursor.fetchone()[0]

        return paste_content_count > 0

    def save_paste_reference(self, key, size, timestamp, expires, title, syntax, user):
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO paste
              (paste_key, timestamp, size, expires, title, syntax, user)
            VALUES
              (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                key,
                timestamp,
                size,
                expires,
                title,
                syntax,
                user,
            )
        )

        logger.debug('persisted paste reference for paste `%s`', key)

        self.connection.commit()

    def save_paste_content(self, key, content):
        self.connection.execute(
            '''
            INSERT OR REPLACE INTO paste_content
              (paste_key, raw_content)
            VALUES
              (?, ?)
            ''',
            (
                key,
                content,
            )
        )

        logger.debug('persisted paste content for paste `%s`', key)