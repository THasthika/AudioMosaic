#!/bin/bash

DB_PATH=./.test_db.db
DATABASE_URL=sqlite:///$DB_PATH
APP_DIST_PATH=./frontend

rm -f $DB_PATH

DATABASE_URL=$DATABASE_URL poetry run alembic upgrade head
APP_DIST_PATH=$APP_DIST_PATH DATABASE_URL=$DATABASE_URL poetry run pytest app/tests_e2e

# clear storage created
rm -r storage/audio_samples/*