#!/bin/bash
# Convert all RAW files in directory to AU with same filename
for f in *.raw
do 
    sox -r 8000 -e signed -b 16 -c 1 "$f" "${f%.*}".au
done