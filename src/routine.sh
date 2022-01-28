#!/bin/bash

DIR="/media/labfiles/lab-exps"
DIREXCLUDE="/media/labfiles/lab-exps/exp-h5-files"

inotifywait -m -q -r -e close $DIR --exclude $DIREXCLUDE| while read DIRECTORY EVENT FILE; 
do 
    case $EVENT in 
        CLOSE_WRITE,CLOSE*)
            echo "file $FILE changed in $DIRECTORY"
            python labexp.py $DIRECTORY
            ;;
    esac
done