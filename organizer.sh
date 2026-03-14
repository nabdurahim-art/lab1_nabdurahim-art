#!/bin/bash

ARCHIVE_DIR="archive"
FILE="grades.csv"
LOG="organizer.log"

# create archive directory if not exists
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir archive
fi

# generate timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# new filename
new_name="grades_$timestamp.csv"

# move and rename
mv $FILE $ARCHIVE_DIR/$new_name

# create new empty csv
touch grades.csv

# log the action
echo "$timestamp | $FILE -> $ARCHIVE_DIR/$new_name" >> $LOG

echo "Archive completed."
