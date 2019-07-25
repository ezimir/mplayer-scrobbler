# -*- coding: utf-8 -*-



import os.path
import sqlite3

from datetime import datetime, timedelta



DB_CREATE = """
    CREATE TABLE tracks (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `artist` TEXT,
        `title` TEXT,
        `source` TEXT,
        `played_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `playback_done_at` TIMESTAMP
    );
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
            `played_at` DESC
        LIMIT 1;
"""



DEFAULT_DURATION = 3 * 60  # assume default track length is 3 minutes



class DBContext(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.connection = sqlite3.connect(
            self.file_path,
            detect_types = sqlite3.PARSE_DECLTYPES,
        )
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

        columns = ", ".join([f"`{column}`" for column in kwargs.keys()])
        values = ", ".join([f":{column}" for column in kwargs.keys()])

        query = f"""
            INSERT INTO tracks
                ({columns})
            VALUES
                ({values});
        """

        with self.dbcontext as c:
            c.execute(query, kwargs)
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

        kwargs["track_id"] = track_id
        with self.dbcontext as c:
            c.execute(query, kwargs)

    def can_submit(self, artist, title):
        """Check whether given track details can be scrobbled."""

        last = self._select(DB_SELECT_LAST_TRACK)
        if not last:
            return True

        last = last[0]

        if last["artist"] == artist and last["title"] == title:
            playback_done = last["playback_done_at"]
            if not playback_done:
                playback_done = last["played_at"] + timedelta(seconds = DEFAULT_DURATION)

            now = datetime.utcnow().replace(microsecond = 0)
            # only allow re-scrobble of last track, if expected duration already passed
            if now > playback_done:
                return True

            return False

        return True


