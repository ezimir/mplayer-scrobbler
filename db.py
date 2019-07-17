# -*- coding: utf-8 -*-



import os.path
import sqlite3



DB_CREATE = """
    CREATE TABLE tracks (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `artist` TEXT,
        `title` TEXT,
        `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP
    );
"""

DB_INSERT = """
    INSERT INTO tracks
        (`artist`, `title`)
    VALUES
        (:artist, :title);
"""

DB_SELECT_LAST = """
    SELECT
        *
    FROM tracks
        ORDER BY
            timestamp DESC
        LIMIT 1;
"""



class TrackDB(object):
    """Wrapper for handling SQLite DB file."""

    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.isfile(file_path):
            self.create_db()

    def _query(self, query, **kwargs):
        """Execute query with given parameters."""

        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        c.execute(query, kwargs)
        conn.commit()
        conn.close()

    def _select(self, query, **kwargs):
        """Execute select with given parameters and return list of dictionaries."""

        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        c.execute(query, kwargs)
        results = c.fetchall()
        columns = [name for (name, *_) in c.description]
        conn.commit()
        conn.close()

        return [dict(zip(columns, result)) for result in results]

    def create_db(self):
        """Execute DB creation query."""

        self._query(DB_CREATE)

    def insert(self, **kwargs):
        """Execute insert query with given track info."""

        self._query(DB_INSERT, **kwargs)

    def can_submit(self, artist, title):
        """Checke whether given track details can be scrobbled."""

        last = self._select(DB_SELECT_LAST)
        if not last:
            return True

        last = last[0]

        if last['artist'] == artist and last['title'] == title:
            return False

        return True


