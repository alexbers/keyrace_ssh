#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}")"

killall tmux 2>/dev/null

rm progress/* 2>/dev/null
rm gameprepare 2>/dev/null
rm gamestarted 2>/dev/null
rm text.txt 2>/dev/null

echo "The game is stopped"