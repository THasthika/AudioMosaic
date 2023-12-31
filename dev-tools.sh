#!/bin/bash

DATABASE_URL=sqlite:///.data.db

# Define the _make_migration function
_make_migration() {
    if [ $# -lt 1 ]; then
        echo "Usage: make_migration <migration message>"
        exit 1
    fi
    # Call alembic revision command with the provided string
    DATABASE_URL=$DATABASE_URL poetry run alembic revision --autogenerate -m "$1"
}

_migrate_up() {
    DATABASE_URL=$DATABASE_URL poetry run alembic upgrade head
}

_run() {
    (cd ./frontend && pnpm run build)
    DATABASE_URL=$DATABASE_URL poetry run uvicorn app.main:app --reload
}

_clear_storage() {
    rm -r storage/audio_samples/*
}

# Check if the argument count is less than 1
if [ $# -lt 1 ]; then
    echo "Usage: $0 <command>"
    exit 1
fi

# Retrieve the command from the second command-line argument
command="$1"

shift

case "$command" in
    make_migration)
        _make_migration "$@"
        ;;
    migrate_up)
        _migrate_up
        ;;
    run)
        _run
        ;;
    clear_storage)
        _clear_storage
        ;;
    # # Add more commands here
    # other_command)
    #     # Handle other_command
    #     ;;
    *)
        echo "Invalid command: $command"
        exit 1
        ;;
esac