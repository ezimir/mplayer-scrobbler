#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import re
import sys


def analyze(stream_info):
    """Process ICY info and trigger DB save if one of recognized formats was used."""

    info_re = r".*?StreamTitle='(?P<info>.*?)'.*?"
    info_match = re.match(info_re, stream_info)
    if not info_match:
        return

    info = info_match.groupdict()["info"]

    recognized_patterns = [
        "(?P<artist>.*)\s*-\s*(?P<title>.*)",  # basic Track - Title format
    ]

    for pattern in recognized_patterns:
        pattern_match = re.match(pattern, info)
        if pattern_match:
            print("TRACK DETECTED: {}".format(pattern_match.groupdict()))


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


