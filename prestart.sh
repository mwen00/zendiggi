#! /usr/bin/env bash

# Let the DB start
python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
# Not necessary right now, not seeding any data
# python ./app/initial_data.py
