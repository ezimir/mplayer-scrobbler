#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re
import sqlite3
import sys

from analyze import ICYAnalyzer


DB_PATH = '/tmp/scrobbles.db'

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


def submit(artist, title):
    """Save track info into external DB for later processing."""

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(DB_INSERT, locals())
    conn.commit()
    conn.close()
    print(f" - Saved for scrobbling: {artist} - {title}")


def capture():
    """Read from stdin and trigger ICY analysis if mplayer outputs it."""

    analyzer = ICYAnalyzer(trigger_callback = submit)

    buff = ""
    while True:
        char = sys.stdin.read(1)
        sys.stdout.write(char)
        if char == "\x1b":
            sys.stdout.flush()

        buff += char
        if buff.endswith("\n"):
            analyzer.process(buff)
            buff = ""

        if "(Quit)" in buff or "(End of file)" in buff:
            break

        if len(buff) > 1000:
            buff = ""


if __name__ == "__main__":
    try:
        capture()

    except KeyboardInterrupt:
        print("Bye.")

