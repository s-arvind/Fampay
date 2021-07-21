#!/bin/sh

exec 2>&1 poetry run python -m sql_migration.migrate
