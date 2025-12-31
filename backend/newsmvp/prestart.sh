#!/usr/bin/env bash

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Run apply migrations.."
    alembic upgrade head
    echo "Migrations applied!"
else
    echo "Skipping migrations..."
fi

exec "$@"