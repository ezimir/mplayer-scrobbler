#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import sys


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
                print(f"Got ICY INFO: {buff}")

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


