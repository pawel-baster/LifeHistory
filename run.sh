#!/bin/bash
sleep 1
#MYDIR="$(dirname "$(realpath "$0")")"
#echo $MYDIR
cd "$(dirname "$0")"
python controller.py
