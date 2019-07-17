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

DB_SELECT_LAST_INSERT_ID = """
    SELECT
        seq
    FROM sqlite_sequence
    WHERE name="tracks";
"""

DB_SELECT_LAST_TRACK = """
    SELECT
        *
    FROM tracks
        ORDER BY
            timestamp DESC
        LIMIT 1;
"""


class DBContext(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.file_path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        self.connection.close()


class TrackDB(object):
    """Wrapper for handling SQLite DB file."""

    def __init__(self, file_path):
        self.dbcontext = DBContext(file_path)

        if not os.path.isfile(file_path):
            self._query(DB_CREATE)

    def _query(self, query, **kwargs):
        """Execute query with given parameters."""

        with self.dbcontext as c:
            c.execute(query, kwargs)

    def _select(self, query, **kwargs):
        """Execute select with given parameters and return list of dictionaries."""

        with self.dbcontext as c:
            c.execute(query, kwargs)
            results = c.fetchall()
            columns = [name for (name, *_) in c.description]

        return [dict(zip(columns, result)) for result in results]

    def insert(self, **kwargs):
        """Execute insert query with given track info."""

        with self.dbcontext as c:
            c.execute(DB_INSERT, kwargs)
            c.execute(DB_SELECT_LAST_INSERT_ID)
            last_id = c.fetchone()
            return last_id[0]

    def update(self, track_id, **kwargs):
        """Execute update query for selected track with given track info."""

        columns = [f"`{column}`=:{column}" for column in kwargs.keys()]
        columns = ", ".join(columns)
        query = f"""
            UPDATE
                tracks
            SET
                {columns}
            WHERE
                id=:track_id;
        """

        kwargs['track_id'] = track_id
        with self.dbcontext as c:
            c.execute(query, kwargs)

    def can_submit(self, artist, title):
        """Check whether given track details can be scrobbled."""

        last = self._select(DB_SELECT_LAST_TRACK)
        if not last:
            return True

        last = last[0]

        if last['artist'] == artist and last['title'] == title:
            return False

        return True


