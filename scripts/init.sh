#!/bin/bash

# create data directories
mkdir ../Adler/data/
mkdir ../Adler/data/data_objects/
mkdir ../Adler/data/data_objects/samples
mkdir ../Adler/data/techtc300_preprocessed/
echo "Data directories created"

# download and unzip data
DATA_URL="http://techtc.cs.technion.ac.il/techtc300/data/techtc300_preprocessed.zip"

wget $DATA_URL -P ../Adler/data/
echo "Data downloaded"

unzip ../Adler/data/techtc300_preprocessed.zip -d ../Adler/data/techtc300_preprocessed/
echo "Data unzipped"

# get category listing
LISTING_URL="http://techtc.cs.technion.ac.il/techtc300/techtc300.html"
wget $LISTING_URL -O ../Adler/data/Tech300Categories.html
echo "Category listing fetched"