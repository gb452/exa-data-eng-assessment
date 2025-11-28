"""
Utility code to get a connection to the postgres database

I consider this boilerplate code, so the AI helped with generating this.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_db_engine() -> Engine:
    """
    Get a connection to the database
    
    :return: sqlalchemy.engine.Engine instance
    """
    db_host = os.getenv('DATABASE_HOSTNAME')
    db_port = os.getenv('DATABASE_PORT')
    db_name = os.getenv('DATABASE_NAME')
    db_user = os.getenv('DATABASE_USERNAME')
    db_pass = os.getenv('DATABASE_PASSWORD')

    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(db_url)
    return engine

