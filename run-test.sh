#!/bin/bash

DB_PATH=./.test_db.db
DATABASE_URL=sqlite:///$DB_PATH

rm -f $DB_PATH

(cd ./frontend && pnpm install && pnpm run build)
DATABASE_URL=$DATABASE_URL poetry run alembic upgrade head
DATABASE_URL=$DATABASE_URL poetry run pytest