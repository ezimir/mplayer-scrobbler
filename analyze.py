# -*- coding: utf-8 -*-



import re



class ICYAnalyzer(object):
    """Wrapper for handling ICY text analysis."""

    name_re = r"Name\s+:\s+(?P<name>.*)"
    info_re = r".*?StreamTitle='(?P<info>.*?)';"

    track_patterns = [
        "(?P<artist>.*)\s+-\s+(?P<title>.*) on AH.FM",      # afterhours.fm
        "(?P<artist>.*)\s+pres\s+(?P<title>.*) on AH.FM",   # alternative track separator for afterhours.fm
        "(?P<artist>.*)\s+-\s+(?P<title>.*?)\s+\[[^[]+\]",  # tracks with notes in square brackets after title
        "\s?-\s+(?P<artist>.*)\s+-\s+(?P<title>.*)",        # tracks with extra dash in front of artist
        "(?P<artist>.*)\s+-\s+(?P<title>.*)",               # basic "Track - Title" format
    ]

    # strings to ignore (station info, ads, ...)
    omit_patterns = [
        "^DrumandBass\.FM.*",
    ]

    source = None

    def __init__(self, trigger_callback):
        self.submit = trigger_callback

    def process(self, text):
        """Decide whether to proceed with ICY parsing or ignore given mplayer output text."""

        if "Name" in text:
            self.analyze_source(text)

        if "ICY" in text:
            self.analyze_track(text)

    def analyze_source(self, stream_info):

        name_match = re.match(self.name_re, stream_info)
        if not name_match:
            return

        self.source = name_match.groupdict()['name']

    def analyze_track(self, stream_info):
        """Process ICY info and trigger DB save if one of recognized formats was used."""

        info_match = re.match(self.info_re, stream_info)
        if not info_match:
            return

        info = info_match.groupdict()["info"]

        for pattern in self.omit_patterns:
            pattern_match = re.match(pattern, info, re.IGNORECASE)
            if pattern_match:
                return

        for pattern in self.track_patterns:
            pattern_match = re.match(pattern, info)
            if not pattern_match:
                continue
            track_kwargs = pattern_match.groupdict()
            if not track_kwargs["artist"] or not track_kwargs["title"]:  # may capture empty strings from texts like " - "
                continue
            self.submit(**self.get_submit_kwargs(track_kwargs))
            break

    def get_submit_kwargs(self, extra_kwargs):
        """Created dictionary with track info arguments to be used for track submission to DB and through LastFM API."""

        kwargs = {
            "source": self.source,
        }
        kwargs.update(extra_kwargs)
        return kwargs

