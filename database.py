import os
import psycopg2

import logging

DATABASE_URL = os.environ['DATABASE_URL']

logger = logging.getLogger(__name__)


def save(filename: str, content: str):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    if exists(filename):
        query = "update textfiles set content = %s where filename = %s"
    else:
        query = "insert into textfiles (content, filename) values (%s, %s)"

    cursor.execute(query, (content, filename))
    if cursor.rowcount != 1:
        logger.log(logging.ERROR, f"Saving of filename {filename} went "
                                  f"wrong.")


def load(filename: str):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    query = "select content from textfiles where filename = %s"
    cursor.execute(query, (filename,))
    content = cursor.fetchone()
    if content:
        return content[0]
    else:
        logger.log(logging.ERROR, f"Filename {filename} not found.")
        return ""


def exists(filename: str):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    query = "select filename from textfiles where filename = %s"
    cursor.execute(query, (filename,))
    return cursor.rowcount == 1
