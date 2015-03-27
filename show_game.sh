#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}")"

if [ -z $1 ]; then
	./tmux ls
else
	./tmux bind-key -n C-q detach \; attach-session -r  -t $1
fi
