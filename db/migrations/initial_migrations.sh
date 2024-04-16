#!/bin/bash

# Set database parameters
DB_USER="postgres" # Replace this with your PostgreSQL username
DB_PASSWORD="pass" # Replace this with your PostgreSQL password
DB_HOST="localhost"
DB_PORT="5432"

NEW_DB_NAME="cogitotest"

SQL_SCRIPT_PATH="001_initial_schema.sql"

export PGPASSWORD=$DB_PASSWORD

psql -h $DB_HOST -U $DB_USER -d postgres -p $DB_PORT -c "CREATE DATABASE $NEW_DB_NAME;"
if [ $? -eq 0 ]
then
    echo "Database creation was successful."
else
    echo "Database creation failed." >&2
    exit 1
fi


psql -h $DB_HOST -U $DB_USER -d $NEW_DB_NAME -p $DB_PORT -f $SQL_SCRIPT_PATH
if [ $? -eq 0 ]
then
    echo "Migration was successful."
else
    echo "Migration failed." >&2
fi

unset PGPASSWORD