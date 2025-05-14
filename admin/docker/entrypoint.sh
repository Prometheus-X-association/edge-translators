#!/bin/sh
set -e

if [ "$1" = 'yarn' ]; then
    echo "Starting app in ${APP_ENV} environment.."

    if [ -z "$(ls -A 'node_modules/' 2>/dev/null)" ]; then
        echo "Installing development dependencies.."
        yarn install --frozen-lockfile --non-interactive --dev
        echo "Development dependencies installed ✅"
	fi
fi

exec "$@"