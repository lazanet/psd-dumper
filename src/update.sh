#!/bin/bash

#python3 fetchChampionships.py
#python3 fetchSquads.py
#python3 updatePlayers.py
pushd ..
mkdir -p dumps
cd data
DATE=`date +%Y%m%d`
zip -r "../dumps/PSDDump_$DATE.zip" "."
popd
