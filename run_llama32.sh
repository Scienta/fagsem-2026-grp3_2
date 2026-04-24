#/bin/bash

MODEL='llama3.2:latest'
CDIR=llama32


# Set API URL to local and a dummy key, then launch
export ANTHROPIC_BASE_URL=http://localhost:11434 
export ANTHROPIC_API_KEY=ollama 
#claude --model ollama/<your-model-name>


mkdir -p $CDIR

source set_env.sh

echo `date` > $CDIR/start.txt

export FILE_DIR=${PWD}/$CDIR

export PYTHONPATH=${PWD}/$CDIR:${PYTHONPATH}

echo 'Read CLAUDE.md skatt.md README.md and implement the tax calculator as described' | ollama launch claude --model ${MODEL}

echo `date` > $CDIR/stop.txt
