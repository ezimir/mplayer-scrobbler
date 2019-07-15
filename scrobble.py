# -*- coding: utf-8 -*-



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


class Scrobbler(object):
    """Wrapper for handling track submission to Last.FM"""

    def __init__(self, db_path):
        self.db_path = db_path

    def submit(self, artist, title):
        """Save track info into external DB file for later processing."""

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(DB_INSERT, locals())
        conn.commit()
        conn.close()
        print(f" - Saved for scrobbling: {artist} - {title}")

