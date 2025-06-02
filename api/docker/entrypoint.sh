#!/bin/sh
set -e

if [ "$1" = 'python' ] || [ "$1" = 'uv' ] || [ "$1" = 'uvicorn' ]; then
    
    echo "AI Translator API initializing.."
    echo "Environment : ${APP_ENV}"
    echo "User : $(whoami)"

    if [ -z "$(ls -A '.venv/' 2>/dev/null)" ]; then
        echo "Installing dependencies..."
        echo "Python virtual environment : $(which python)"
        uv sync --frozen
        echo "Dependencies installed."
	else
        echo "Dependencies already installed."
    fi
    
    echo "Start model fetching step..."
    python fetch_model.py
    echo "End model fetching step."
    echo "AI Translator API initialized."
fi

exec "$@"
