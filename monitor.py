#!/usr/bin/python3

import os
import os.path
import time
import datetime
import glob

GAMESTARTED_FILENAME = "gamestarted"
GAMEPREPARE_FILENAME = "gameprepare"

PREPARE_TIME = 10
PROGRESS_WIDTH = 50
MAX_NAME_LEN = 20

FONT = [
"  __  #    # __  # __  #      #  __ #  __  # ___ #  __  #  __  # # #   ",
" /  \ # /| #  _) #  _) # |__| # |_  # /__  #   / # (__) # (__\ #.# #__ ",
" \__/ #  | # /__ # __) #    | # __) # \__) #  /  # (__) #  __/ #.#.#   ",
]

def render_time(time_str, line_num):
    chr2fontpos = {}
    for i in range(10):
        chr2fontpos[str(i)] = i
    chr2fontpos[":"] = 10
    chr2fontpos["."] = 11
    chr2fontpos["-"] = 12

    pieces = FONT[line_num].split("#")

    print(" " * 35, end="")
    # print("\033[1m", end="")
    for c in time_str:
        if c not in chr2fontpos:
            continue

        print(pieces[chr2fontpos[c]], end="")
    print("\033[0m")

def render_progress(graph_progress):
    print("[", end="")

    drawed = max(0, graph_progress - 1)
    print("=" * drawed, end="")
    if graph_progress != PROGRESS_WIDTH:
        print(">", end="")
    else:
        print("=", end="")
    drawed += 1


    print(" " * min(PROGRESS_WIDTH - drawed, PROGRESS_WIDTH), end="")
    print("] ", end="")


def is_game_started():
    try:
        open(GAMESTARTED_FILENAME)
        return True
    except:
        return False

def loop():
    try:
        gamestart_time = os.path.getmtime(GAMESTARTED_FILENAME)
    except:
        try:
            gamestart_time = os.path.getmtime(GAMEPREPARE_FILENAME) + PREPARE_TIME
            if gamestart_time < time.time():
                gamestart_time = None
        except:
            gamestart_time = None

    
    if gamestart_time is None:
        time_str = "-%01d:%04.1f" % (0, PREPARE_TIME)
    else:
        minutes, seconds = divmod(abs(time.time() - gamestart_time), 60)
        time_str = "%01d:%04.1f" % (minutes, seconds)
        if time.time() - gamestart_time < 0:
            time_str = "-" + time_str

    render_time(time_str, 0)
    render_time(time_str, 1)
    render_time(time_str, 2)
    print()

    try:
        strings_in_file = len(open("text.txt").readlines())
        bytes_in_file = os.path.getsize("text.txt")
    except:
        strings_in_file = 100000

    # print(strings_in_file)

    name2progress = {}

    for path in glob.glob("./progress/*"):
        try:
            progress = int(open(path).readline().strip())
        except:
            progress = 0
        name = os.path.basename(path)

        name2progress[name] = progress

    can_stop = True

    for name in sorted(name2progress.keys()):
        progress = name2progress[name]
        graph_progress = int((progress / strings_in_file) * PROGRESS_WIDTH)

        if progress == strings_in_file:
            graph_progress = PROGRESS_WIDTH
        else:
            can_stop = False

        print(name.rjust(MAX_NAME_LEN) + ": ", end="")

        render_progress(graph_progress)

        if progress == strings_in_file:
            try:
                result = os.path.getmtime("./progress/" + name) - gamestart_time
                minutes, seconds = divmod(result, 60)
                result_str = "%01d:%04.1f" % (minutes, seconds)
                print(result_str, end=", ")

                chars_in_min = int((bytes_in_file / result) * 60)
                print("%d chars/min" % chars_in_min, end="")
            except E:
                print(E)
        print()

    if can_stop:
        time.sleep(10000)


while True:
    try:
        os.system("clear")
        loop()
    except:
        raise
    finally:
        time.sleep(0.1)

