# -*- coding: utf-8 -*-



import sys

from analyze import ICYAnalyzer
from scrobble import Scrobbler



def capture():
    """Read from stdin and pass mplayer output to ICY text analyzer."""

    scrobbler = Scrobbler('/tmp/scrobbles.db')
    analyzer = ICYAnalyzer(trigger_callback = scrobbler.submit)

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

