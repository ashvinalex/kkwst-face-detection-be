#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" /TodoApp/"
cd $SCRIPT_DIR

# Kill all process running port 8001
echo "Killed processes: $(lsof -t -i tcp:8001)" && lsof -t -i tcp:8001 | xargs kill -9

echo "Starting Server......"
# To Run the server with reload
uvicorn main:app --host 127.0.0.1 --port 8001

# uvicorn main:app --host 127.0.0.1 --port 8000