#!/bin/bash

DATA_URL="http://techtc.cs.technion.ac.il/techtc100/data/techtc100_preprocessed.zip"

# create data directories
mkdir ../Adler/data/
mkdir ../Adler/data/techtc100_preprocessed/
echo "Data directories created"

# download and unzip data
wget $DATA_URL -P ../Adler/data/
echo "Data downloaded"

unzip ../Adler/data/techtc100_preprocessed.zip -d ../Adler/data/techtc100_preprocessed/
echo "Data unzipped"