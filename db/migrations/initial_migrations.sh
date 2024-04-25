#!/bin/bash

# Load environment variables
set -o allexport
source ../.env
set +o allexport

NEW_DB_NAME="$DB_NAME"

SQL_SCRIPT_PATH="001_initial_schema.sql"

export PGPASSWORD=$DB_PASSWORD

# Create a new database
psql -h $DB_HOST -U $DB_USER -d postgres -p $DB_PORT -c "CREATE DATABASE $NEW_DB_NAME;"
if [ $? -eq 0 ]
then
    echo "Database creation was successful."
else
    echo "Database creation failed." >&2
    exit 1
fi

# Run the migration SQL script to setup tables and relationships
psql -h $DB_HOST -U $DB_USER -d $NEW_DB_NAME -p $DB_PORT -f $SQL_SCRIPT_PATH
if [ $? -eq 0 ]
then
    echo "Migration was successful."
else
    echo "Migration failed." >&2
fi

unset PGPASSWORD
unset NEW_DB_NAME
