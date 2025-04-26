"""
This script resets the SQLAlchemy database to contain a greater abundance
of data than `test_reset.py` for greater UI testing.

Previously, we duplicated data between testing and this database reset.
Moving forward, we'll aim to have some parity between tests and dev reset.
This way, we both avoid duplication and make it easier to interact with
the state of the system we are writing tests for.

Usage: python3 -m script.reset_demo
"""

import sys
import subprocess
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

# from ..tests.services import user_data, post_data

# Ensures that the script can only be run in development mode
if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

# Run Delete and Create Database Scripts
subprocess.run(["python3", "-m", "backend.script.delete_db"])
subprocess.run(["python3", "-m", "backend.script.create_db"])

# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)

# Initialize the SQLAlchemy session
# with Session(engine) as session:
#     # Load all demo data
#     user_data.insert_fake_data(session)
#     post_data.insert_fake_data(session)
#     # Commit changes to the database
#     session.commit()
