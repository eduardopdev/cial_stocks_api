import logging
import psycopg2
from django.conf import settings

class PostgresHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        self.connection.autocommit = True

    def emit(self, record):
        cursor = self.connection.cursor()
        log_entry = self.format(record)
        cursor.execute("INSERT INTO stocks_api_requestlog (level, message) VALUES (%s, %s)",
                       (record.levelname, log_entry))
        cursor.close()