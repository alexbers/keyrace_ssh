#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}")"

set -e

if [ -f gamestarted -o -f gameprepare ]; then
	echo "Old game is still running, run ./stop_game.sh"
	exit 1
fi

text=${1:?usage: start.game.sh <textfile>}

text_data=$(<$text)
touch gameprepare
echo "Get ready!!"
for i in {15..1}; do
    echo $i
    sleep 1
done

echo "$text_data" > text.txt

touch gamestarted
echo "Go!Go!Go!"

#echo "Press Ctrl-C to stop the game"
#trap "./stop_game.sh" SIGINT SIGTERM

#while true; do
#    sleep 600
#done
#echo Game was running too long. Stopping it
#./stop_game.sh
