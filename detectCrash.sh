#!/bin/sh
while true 
do
    if ps -p $(cat p.pid) > /dev/null 
    then
        sleep 10
    else
        echo "Indmelding til opgave robotten er crashet." | mailx -s "Crash detected" $(cat emails.txt) 
        exit 0
    fi
done
