# -*- coding: utf-8 -*-



import json
import pylast

from datetime import datetime

from db import TrackDB



class Scrobbler(object):
    """Wrapper for handling track submission to Last.FM."""

    def __init__(self, db_path, creds_path):
        self.db = TrackDB(db_path)
        self.creds_path = creds_path

    def save_to_db(self, artist, title):
        """Save given track details to local DB."""

        self.db.insert(artist, title)
        print(f" - Saved for scrobbling: {artist} - {title}")

        return True  # TODO: detect duplicates, etc.

    def scrobble(self, artist, title):
        """Submit given track details to Last.FM."""

        creds = json.load(open(self.creds_path))

        api = pylast.LastFMNetwork(
            api_key = creds["APIKey"],
            api_secret = creds["APISecret"],
            username = creds["UserName"],
            password_hash = creds["PasswordHash"],
        )

        timestamp = int(datetime.now().timestamp())
        api.scrobble(artist, title, timestamp)
        track = api.get_track(artist, title)
        print(f" - Scrobbled: {track}")

    def submit(self, artist, title):
        """Process track info (save locally and submit if possible)."""

        safe_to_submit = self.save_to_db(artist, title)
        if safe_to_submit:
            self.scrobble(artist, title)

