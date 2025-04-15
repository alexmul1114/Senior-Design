#!/bin/bash

# This script downloads the first n .tif images from the ship_detection_testdata aws bucket to the current directory. 
# Pass n as the first command line arg when running the script, for example:
# bash download.sh 10
# Note that each image is hundreds of MB

NUM_IMAGES=$1
BUCKET="umbra-open-data-catalog"
PREFIX="sar-data/tasks/ship_detection_testdata"
DEST_DIR="tif-images"

mkdir -p "$DEST_DIR"

# List the first 20 top-level folders in the prefix.
folders=$(aws s3 ls s3://$BUCKET/$PREFIX/ --no-sign-request | awk '/PRE/ {print $2}' | head -n 200)

downloaded=0
for folder in $folders; do
    # Remove trailing slash from folder name
    folder=${folder%/}
    echo "Processing folder: $folder"

    # List all .tif files in this folder and subfolders recursively.
    tif_files=$(aws s3 ls s3://$BUCKET/$PREFIX/$folder/ --recursive --no-sign-request | awk '$4 ~ /\.tif$/ {print $4}')
    
    # Loop over each found .tif file
    for tif in $tif_files; do
         # Don't redownload
         if [ $downloaded -ge $NUM_IMAGES ]; then
              echo "Downloaded $downloaded images; reached the limit of $NUM_IMAGES."
              exit 0
         fi

         # Create local directory structure 
         local_path="$DEST_DIR/$tif"
         mkdir -p "$(dirname "$local_path")"
         
         echo "Downloading s3://$BUCKET/$tif to $local_path"
         aws s3 cp s3://$BUCKET/$tif "$local_path" --no-sign-request
         
         downloaded=$((downloaded + 1))
    done
done

echo "Download complete. Total images downloaded: $downloaded"