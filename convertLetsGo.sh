#!/bin/bash

if [ $# -ne 2 ]; then
    name=$0
    echo "Usage: $name INPUT_DIR OUTPUT_DIR"
    echo "Convert all '...input.raw' and '...input_and_output.raw' files in INPUT_DIR to AU and save to OUTPUT_DIR"
    exit 1
fi

mkdir -p $2

find $1 -regextype awk -iregex '.*/.*input(_and_output)?\.raw' | while read file ; do
    file_basename=$(basename "$file" .raw)
    echo "$file_basename"
    sox -r 8000 -e signed -b 16 -c 1 "$file" $2/$file_basename.au
done
