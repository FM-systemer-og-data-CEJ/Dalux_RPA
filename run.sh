#!/bin/sh
rm nohup.out
nohup python3 -u src/main.py $1 &
echo $! > p.pid