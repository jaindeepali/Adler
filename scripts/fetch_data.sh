#!/bin/bash

DATA_URL="http://techtc.cs.technion.ac.il/techtc300/data/techtc300_preprocessed.zip"

# create data directories
mkdir ../Adler/data/
mkdir ../Adler/data/techtc300_preprocessed/
echo "Data directories created"

# download and unzip data
wget $DATA_URL -P ../Adler/data/
echo "Data downloaded"

unzip ../Adler/data/techtc300_preprocessed.zip -d ../Adler/data/techtc300_preprocessed/
echo "Data unzipped"

# for category listing
LISTING_URL="http://techtc.cs.technion.ac.il/techtc300/techtc300.html"
wget $LISTING_URL -O ../Adler/data/Tech300Categories.html