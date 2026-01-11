#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

# Initialize database
python -c "from run import db; db.create_all()"
