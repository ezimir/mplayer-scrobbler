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



class TrackDB(object):


    def __init__(self, file_path):
        self.file_path = file_path

    def insert(self, artist, title):
        conn = sqlite3.connect(self.file_path)
        c = conn.cursor()
        c.execute(DB_INSERT, locals())
        conn.commit()
        conn.close()
