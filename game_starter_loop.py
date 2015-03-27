#!/usr/bin/python3

import os
import os.path
import time
import glob
import random
import traceback

from subprocess import call

GAMESTARTED_FILENAME = "gamestarted"
GAMEPREPARE_FILENAME = "gameprepare"

MAX_GAME_DURATION = 10 * 60
INACTIVITY_TIMEOUT = 60


def is_game_running():
    return os.path.isfile(GAMEPREPARE_FILENAME) or os.path.isfile(GAMESTARTED_FILENAME)


def start_game():
    textfile = random.choice(glob.glob("./texts/*"))
    call(["./start_game.sh", textfile])


def stop_game():
    call(["./stop_game.sh"])


def is_game_expired():
    try:
        gameprepare_time = os.path.getmtime(GAMEPREPARE_FILENAME)
        return abs(time.time() - gameprepare_time) > MAX_GAME_DURATION
    except Exception:
        traceback.print_exc()
        return True


def is_all_finished():
    try:
        strings_in_file = len(open("text.txt").readlines())
    except Exception:
        return True

    for path in glob.glob("./progress/*"):
        try:
            progress = int(open(path).readline().strip())
            if progress < strings_in_file:
                return False
        except:
            traceback.print_exc()
            return True
    return True


def is_nobody_playing():
    max_mod_time = 0
    for path in glob.glob("./progress/*"):
        try:
            max_mod_time = max(max_mod_time, os.path.getmtime(path))
        except:
            traceback.print_exc()
            return True

    return abs(time.time() - max_mod_time) > INACTIVITY_TIMEOUT


def loop():
    if not is_game_running():
        # is anyone here to play
        if not glob.glob("./progress/*"):
            print("No one is here, delaying start")
            return

        print("Staring game")
        time.sleep(5)
        start_game()
    else:
        if is_game_expired():
            print("Stoping expired game")
            stop_game()
        if is_all_finished():
            print("Stoping the game because all is finished")
            time.sleep(20)
            stop_game()
        if is_nobody_playing():
            print("Stoping tha game because no one playing")
            stop_game()


while True:
    try:
        loop()
    except:
        traceback.print_exc()
    finally:
        time.sleep(5)
