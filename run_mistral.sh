#/bin/bash

mkdir -p mistral

echo `date` > mistral/start.txt

export FILE_DIR=${PWD}/mistral

ollama launch 

echo `date` > mistral/stop.txt


