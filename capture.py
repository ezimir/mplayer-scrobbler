#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re
import sqlite3
import sys


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


def analyze(stream_info):
    """Process ICY info and trigger DB save if one of recognized formats was used."""

    info_re = r".*?StreamTitle='(?P<info>.*?)'.*?"
    info_match = re.match(info_re, stream_info)
    if not info_match:
        return

    info = info_match.groupdict()["info"]

    recognized_patterns = [
        "(?P<artist>.*)\s+-\s+(?P<title>.*)",  # basic Track - Title format
    ]

    for pattern in recognized_patterns:
        pattern_match = re.match(pattern, info)
        if pattern_match:
            submit(**pattern_match.groupdict())


def capture():
    """Read from stdin and trigger ICY analysis if mplayer outputs it."""

    buff = ""
    while True:
        char = sys.stdin.read(1)
        sys.stdout.write(char)
        if char == "\x1b":
            sys.stdout.flush()

        buff += char
        if buff.endswith("\n"):
            if "ICY" in buff:
                analyze(buff)

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

