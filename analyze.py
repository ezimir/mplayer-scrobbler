# -*- coding: utf-8 -*-



import re



class ICYAnalyzer(object):
    """Wrapper for handling ICY text analysis."""

    def __init__(self, trigger_callback):
        self.submit = trigger_callback

    def process(self, text):
        """Decide whether to proceed with ICY parsing or ignore given mplayer output text."""

        if "ICY" in text:
            self.analyze(text)

    def analyze(self, stream_info):
        """Process ICY info and trigger DB save if one of recognized formats was used."""

        info_re = r".*?StreamTitle='(?P<info>.*?)'.*?"
        info_match = re.match(info_re, stream_info)
        if not info_match:
            return

        info = info_match.groupdict()["info"]

        recognized_patterns = [
            "(?P<artist>.*)\s+-\s+(?P<title>.*) on AH.FM",  # afterhours.fm
            "(?P<artist>.*)\s+-\s+(?P<title>.*)",  # basic Track - Title format
        ]

        for pattern in recognized_patterns:
            pattern_match = re.match(pattern, info)
            if pattern_match:
                self.submit(**pattern_match.groupdict())
                break

