# -*- coding: utf-8 -*-



import argparse
import sys

from analyze import ICYAnalyzer
from scrobble import Scrobbler


parser = argparse.ArgumentParser(description = "Scrobble tracks from mplayer stream to Last.FM.")
parser.add_argument("credentials", help = "path to Last.FM credentials file")



def capture(args):
    """Read from stdin and pass mplayer output to ICY text analyzer."""

    scrobbler = Scrobbler('/tmp/scrobbles.db', args.credentials)
    analyzer = ICYAnalyzer(trigger_callback = scrobbler.submit)

    buff = ""

    while True:
        try:
            char = sys.stdin.read(1)
        except UnicodeDecodeError:
            char = ""

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
        args = parser.parse_args()
        capture(args)

    except KeyboardInterrupt:
        print("Bye.")

