#!/bin/sh

exec 2>&1 poetry run python -m cron_script.sync_data
