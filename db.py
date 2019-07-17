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



class TrackDB(object):


    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.isfile(file_path):
            self.create_db()

    def _query(self, query, *args, **kwargs):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        c.execute(query, *args, **kwargs)
        conn.commit()
        conn.close()

    def create_db(self):
        self._query(DB_CREATE)

    def insert(self, artist, title):
        self._query(DB_INSERT, locals())

