#!/bin/bash
set -e

# Run the database migrations
echo "--- Running database migrations ---"
alembic upgrade head

# Start the application server
echo "--- Starting application ---"
uvicorn main:app --host 0.0.0.0 --port 8000
