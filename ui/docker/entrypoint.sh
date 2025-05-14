#!/bin/sh
set -e

if [ "$1" = 'streamlit' ] || [ "$1" = 'python' ]; then
    echo "Application starting.."
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
fi

exec "$@"