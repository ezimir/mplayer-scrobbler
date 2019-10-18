# -*- coding: utf-8 -*-



import json
import pylast

from datetime import datetime, timedelta

from db import TrackDB



class Scrobbler(object):
    """Wrapper for handling track submission to Last.FM."""

    def __init__(self, db_path, creds_path):
        self.db = TrackDB(db_path)

        creds = json.load(open(creds_path))
        self.api = pylast.LastFMNetwork(
            api_key = creds["APIKey"],
            api_secret = creds["APISecret"],
            username = creds["UserName"],
            password_hash = creds["PasswordHash"],
        )

    def scrobble(self, artist, title):
        """Submit given track details to Last.FM."""

        timestamp = int(datetime.now().timestamp())
        self.api.scrobble(artist, title, timestamp)

        track = self.api.get_track(artist, title)
        print(f" - Scrobbled: {track}")
        return track

    def submit(self, artist, title, source):
        """Process track info (save locally and submit if possible)."""

        print(f"\33]0;{source}: {artist} - {title}\a", end = "", flush = True)
        if self.db.can_submit(artist, title, source):
            track_id = self.db.insert(
                artist = artist,
                title = title,
                source = source,
            )
            track = self.scrobble(artist, title)

            track_duration = None

            try:
                track_duration = track.get_duration() / 1000

            except pylast.WSError as e:
                print(f" - Exception: {e}")

            if track_duration:
                now = datetime.utcnow().replace(microsecond = 0)
                playback_done = now + timedelta(seconds = track_duration)
                self.db.update(
                    track_id,
                    playback_done_at = playback_done,
                )

