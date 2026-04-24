#/bin/bash

mkdir -p mistral

source set_env.sh

echo `date` > mistral/start.txt

export FILE_DIR=${PWD}/mistral

export PYTHONPATH=${PWD}/FILE_DIR:${PYTHONPATH}

ollama launch claude --model mistral:latest

echo `date` > mistral/stop.txt
