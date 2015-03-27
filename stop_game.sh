#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}")"

./killall -w tmux 2>/dev/null

rm -f progress/* 2>/dev/null
rm -f gameprepare 2>/dev/null
rm -f gamestarted 2>/dev/null
rm -f text.txt 2>/dev/null

echo "The game is stopped"