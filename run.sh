#!/bin/bash

# Check if a directory path is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Store the directory path
directory="$1"

# Check if the provided path is a directory
if [ ! -d "$directory" ]; then
    echo "Error: $directory is not a directory."
    exit 1
fi

mkdir -p testlocals
rm -f testlocals/*.tf

# Iterate over files ending with .tf
for file in "$directory"/*.tf; do
    # Check if there are matching files
    if [ -e "$file" ]; then
        # Print the filename to stdout
        echo "$file"
	python tflocals.py $file > testlocals/$(basename "$file")

    else
        # Handle case when no matching files are found
        echo "No files found ending with .tf in $directory"
        exit 1
    fi
done

