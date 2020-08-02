import os
import psycopg2

import logging

DATABASE_URL = os.environ['DATABASE_URL']

logger = logging.getLogger(__name__)


def save(filename: str, content: str):
    logger.log(logging.WARN, "entered save method.")
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    if exists(filename):
        logger.log(logging.WARN, "file exists, updating file.")
        query = "update textfiles set content = %s where filename = %s"
    else:
        query = "insert into textfiles (content, filename) values (%s, %s)"

    try:
        logger.log(logging.WARN, f"executing query {query}.")
        cursor.execute(query, (content, filename))
        logger.log(logging.WARN, "done.")
    except Exception as err:
        print(err)

    if cursor.rowcount != 1:
        logger.log(logging.ERROR, f"Saving of filename {filename} went "
                                  f"wrong.")

    conn.commit()
    cursor.close()
    conn.close()


def load(filename: str):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    query = "select content from textfiles where filename = %s"
    cursor.execute(query, (filename,))
    content = cursor.fetchone()

    cursor.close()
    conn.close()
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
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()
    return rowcount == 1
