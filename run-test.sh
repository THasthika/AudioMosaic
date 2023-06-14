DB_PATH=./.test_db.db
DATABASE_URL=sqlite:///$DB_PATH

rm -f $DB_PATH

DATABASE_URL=$DATABASE_URL alembic upgrade head
DATABASE_URL=$DATABASE_URL pytest