import os
from contextlib import contextmanager
import logging

try:
    import psycopg2
except: # This can happen in local envs
    pass


class Database:
    """Abstract class"""
    def __init__(self, config):
        raise NotImplementedError()

    def save(self, filename: str, content: str):
        raise NotImplementedError()

    def load(self, filename: str):
        raise NotImplementedError()

    def exists(self, filename: str):
        raise NotImplementedError()


class PgDatabase(Database):
    def __init__(self, config):
        self.url = config["DATABASE_URL"]
        self.sslmode = config["SSLMODE"]
        self.logger = logging.getLogger(__name__)
        self.connection = None

    @contextmanager
    def _cursor(self):
        """Internal function to start and re-use connections in a single action in safe way."""
        if self.connection is not None: 
            cursor = self.connection.cursor()
            try:
                yield cursor
            finally:
                cursor.close()
            return
        else:
            self.connection = psycopg2.connect(self.url, sslmode=self.sslmode)
            cursor = self.connection.cursor()
            try:
                yield cursor
            finally:
                self.connection.commit()
                cursor.close()
                self.connection.close()
                self.connection = None
            return

    def save(self, filename: str, content: str):
        self.logger.log(logging.INFO, "Database saving")

        with self._cursor() as cursor:
            if self.exists(filename):
                self.logger.log(logging.INFO, f"File {filename} exists, updating.")
                query = "UPDATE textfiles SET content = %s WHERE filename = %s"
            else:
                self.logger.log(logging.INFO, f"Creating new file {filename}")
                query = "INSERT INTO textfiles (content, filename) VALUES (%s, %s)"

            try:
                cursor.execute(query, (content, filename))
            except Exception as err:
                self.logger.log(logging.ERROR, f"Database error occurred: {err}")

            if cursor.rowcount != 1:
                self.logger.log(logging.ERROR, f"Rowcount was not 1 while saving.")

    def load(self, filename: str):
        with self._cursor() as cursor:
            query = "SELECT content FROM textfiles WHERE filename = %s"
            cursor.execute(query, (filename,))
            content = cursor.fetchone()

            if content:
                return content[0]
            else:
                self.logger.log(logging.ERROR, f"Filename {filename} not found.")
                return ""

    def exists(self, filename: str):
        with self._cursor() as cursor:
            query = "SELECT filename FROM textfiles WHERE filename = %s"
            cursor.execute(query, (filename,))
            return cursor.rowcount == 1



class TXTDatabase(Database):
    def __init__(self, config):
        self.url = config["DATABASE_URL"]
        self.logger = logging.getLogger(__name__)

    def save(self, filename: str, content: str):
        self.logger.log(logging.INFO, "Database saving")

        with open(self.url + filename, 'w') as f:
            f.write(content)

    def load(self, filename: str):
        if self.exists(filename):
            with open(self.url + filename) as f:
                return f.read()
        else:
            return ""

    def exists(self, filename: str):
        return os.path.exists(self.url + filename)
