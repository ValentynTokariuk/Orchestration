#!/bin/bash

# This script prints the contents of .yaml, .py, Dockerfile, and .json files in the current directory.

# Define a separator for clarity in output
separator="---------------------------------------------------------------"

# Loop through each type of file and print its contents
for extension in "*.yaml" "*.py" "Dockerfile"
do
    # Check for files matching the current pattern
    files=$(ls $extension 2> /dev/null)
    if [ -z "$files" ]; then
        echo "No files found for pattern $extension"
        continue
    fi

    # Print each file's contents
    for file in $files
    do
        echo "$separator"
        echo "Contents of $file:"
        echo "$separator"
        cat $file
        echo "$separator"  # Add separator after the content
    done
done

# Final separator after the last file
echo "$separator"
