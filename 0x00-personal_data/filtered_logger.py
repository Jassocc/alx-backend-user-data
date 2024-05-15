#!/usr/bin/env python3
"""
script for all tasks
"""
import re
import os
import logging
import mysql.connector
from typing import List


def filter_datum(fields, redaction, message, separator):
    """
    returns the log message
    """
    for field in fields:
        pat = re.sub(f'{i}=.*?{separator}', f'{i}={redaction}{separator}',
                     message)
    return pat


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting fields"""
        record.message = filter_datum(self.fields, self.REDACTION,
                                      record.getMessage(), self.SEPARATOR)
        result = super(RedactingFormatter, self).format(record)
        return result


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    gets logs from csv
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    connects to a secure db
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name_db = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connection.MySQLConnection(user=username,
                                                      password=password,
                                                      host=host,
                                                      database=name_db)


def main():
    """
    main func
    """
    db = get_db()
    curs = db.cursor()
    curs.execute("SELECT * FROM users;")
    f_name = [a[0] for a in curs.description]
    log = get_logger()
    for rows in curs:
        s_rows = ''.join(f'{b}={str(c)}; ' for b, c in zip(rows, f_name))
        log.info(s_rows.strip())
    curs.close()
    db.close()


if __name__ == "__main__":
    main()
