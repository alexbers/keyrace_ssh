#!/bin/bash -i

# change directory to the script location
cd "$( dirname "${BASH_SOURCE[0]}")"

ulimit -v 30000
ulimit -t 30

while true; do
	echo "Welcome to the game!"
	if [ -f gamestarted ]; then
        echo "Game was already started, you can be a spectrator(press ctrl-q to detach)"
        echo "Available names: " $(ls ./progress)

        read -p "Enter player name(enter * for follow the leader): " name

        if [[ "$name" == '*' ]]; then

            # fill backgrounnd with blue
            echo -ne "\e[44m"
            for i in {1..2000}; do
                echo -ne "          "
            done
            echo -ne "\e[0m"

            prev_leader=""

            while true; do
                leader=""
                leader_points="0"
                for player in $(ls ./progress); do
                    points=$(<./progress/${player})
                    if [ "${points}" -gt "${leader_points}" ]; then
                        leader_points="${points}"
                        leader="${player}"
                    fi
                done

                if [ -z "$leader" ]; then
                    sleep 1
                    continue
                fi
                timeout 15 ./show_game.sh "${leader}" 2>/dev/null >/dev/null

                if [[ "${leader}" != "${prev_leader}" ]]; then
                    sleep 1.5
                fi
                prev_leader="${leader}"
                
            done
            continue
        fi

        if [[ ! "$name" =~ ^[0-9a-zA-Z_]{1,20}$ ]]; then
                echo "Bad name"
                continue
        fi

        if [[ ! -f ./progress/${name} ]]; then
        	echo "No such player"
        	echo
        	continue
        fi

        ./show_game.sh "${name}"
        #sleep 1
    else
        read -p "Enter your name: " name

	#if [[ ls progress/* | wc -l -lt 10 ]]; then
	#   echo sorry;
        #fi

        if [[ ! "$name" =~ ^[0-9a-zA-Z_]{1,20}$ ]]; then
                echo "Bad name"
                continue
        fi

        progress_file="./progress/${name}"

        if [ -f "${progress_file}" ]; then
                echo "User exists"
                continue
        fi

		if [ -f gamestarted ]; then
			continue
		fi


        # touch "${progress_file}"
        echo 0 >${progress_file}
        break
    fi
done


PS1=$(echo -e "\033[1m${name}\033[0m # ")

text_file=$(readlink -f text.txt)
# echo $text_file
progress_file=$(readlink -f progress/${name})

timestamp=$(date +%s)
record_file=$(readlink -f rec/${name}_${timestamp}.rec)
timing_file=$(readlink -f rec/${name}_${timestamp}.time)

text_cycle="
export LANG=en_US.UTF-8
while true; do 
 clear

 if [ ! -f gamestarted ]; then 
        echo
        echo ' Game is not started yet'
        sleep 0.1
        continue
 fi
 LINES=\$(tput lines)
 progress=\$(cat ${progress_file})
 progress_start=\$((\$progress+1))
 progress_end=\$((\$progress+\$LINES-1))
 cat ${text_file} | sed -n \"\${progress_start},\${progress_end}s/^/# /p\" # | sed 'y/aocpex/аосрех/'

 inotifywait -e close_write -q -t 10 ${progress_file}
 #sleep 0.1

done
"

./tmux -f tmux.conf new-session -s "${name}" "${text_cycle}" \; set -a status off \; split-window -p 75 "progress_file='${progress_file}' text_file='${text_file}' name='${name}' PS1='${PS1}' script -q --timing='$timing_file' -c './zsh -o NO_GLOBAL_RCS -o NO_RCS' '$record_file'" \; split-window -p 75 -d "./monitor.py"
