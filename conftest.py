"""
Pytest configurations and fixtures for testing.
"""

import pytest
import json
import sys

from os.path import abspath, dirname

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool


# fix imports for the pipeline (normally it will be running in a container)
TEST_DIR = dirname(abspath(__file__))
sys.path.insert(0, dirname(abspath(__file__)) + '/pipeline')

# create an in-memory sqlite db for testing with to replace the postgres db
ENGINE = create_engine("sqlite://")


@pytest.fixture
def test_db_engine():
    """
    Pytest fixture to get the mock database engine.
    
    Used as a monkeypatched replacement for database.get_db_engine
    """
    return lambda: ENGINE


@pytest.fixture
def load_json_fixture():
    """Pytest fixture to load json from a file"""
    def _load(file_path):
        with open(f"{TEST_DIR}/test/test_files/{file_path}", "r") as f:
            return json.load(f)
        
    return _load


@pytest.fixture
def check_table_exists(test_db_engine):
    """Pytest fixture to check if a table exists in the database"""
    def _check(table_name):
        with test_db_engine().connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master "
                f"WHERE type='table' AND name=:name"),
                {"name": table_name}
            )
            return result.fetchone() is not None
    return _check


@pytest.fixture
def check_item_exists_in_table(test_db_engine):
    """Pytest fixture to check if an item exists in a given table in the database"""
    def _check(table_name, item_id):
        with test_db_engine().connect() as connection:
            result = connection.execute(
                text(f'SELECT * FROM "{table_name}" WHERE id = :id'),
                {"id": item_id}
            )
            return result.fetchone() is not None
    return _check
