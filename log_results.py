#!/usr/bin/python3

import os
import time
import glob
import re
import hashlib
import traceback

GAMESTARTED_FILENAME = "gamestarted"
GAMEPREPARE_FILENAME = "gameprepare"
TEXT_FILENAME = "text.txt"


def main():
    text_hash = hashlib.sha256(open(TEXT_FILENAME, "rb").read()).hexdigest()
    strings_in_file = len(open(TEXT_FILENAME).readlines())
    bytes_in_file = os.path.getsize(TEXT_FILENAME)
    
    if bytes_in_file == 0:
        return

    gamestart_time = os.path.getmtime(GAMESTARTED_FILENAME)

    for path in glob.glob("./progress/*"):
        try:
            name = os.path.basename(path)

            if not re.fullmatch(r"[0-9a-zA-Z_]{1,20}", name):
                continue

            progress = int(open(path).readline().strip())

            if progress != strings_in_file:
                continue

            result = os.path.getmtime("./progress/" + name) - gamestart_time
            if result == 0:
                break  # wtf?

            chars_in_min = int((bytes_in_file / result) * 60)

            with open("results.txt", "a") as f:
                f.write(str(int(time.time())) + " " + text_hash + " " + name + " " + str(chars_in_min) + "\n")
        except Exception:
            traceback.print_exc()
            continue


if __name__ == "__main__":
    main()