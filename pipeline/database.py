"""
Utility code for using and accessing the database
"""

from functools import lru_cache

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ProgrammingError, OperationalError

from pandas import json_normalize


# this function is AI generated as it's essentially just boilerplate code
# gets a connection to the db
# (except for lru_cache which I added so that we reuse the connection)
@lru_cache()
def get_db_engine() -> Engine:
    """
    Get a connection to the database
    
    :return: sqlalchemy.engine.Engine instance
    """
    # this will be used for testing, if not set then we will have each
    # part of the url as individual args
    if not (db_url := os.getenv("DATABASE_URL")):
        db_host = os.getenv('DATABASE_HOSTNAME')
        db_port = os.getenv('DATABASE_PORT')
        db_name = os.getenv('DATABASE_NAME')
        db_user = os.getenv('DATABASE_USERNAME')
        db_pass = os.getenv('DATABASE_PASSWORD')

        db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(db_url)
    return engine


def send_object(fhir_object):
    """
    Upload JSON representing the FHIR object to the database
    """

    if fhir_object["data"]:
        engine = get_db_engine()
        # turn into a pandas dataframe
        entry = json_normalize(fhir_object["data"])
        # Below line is AI generated - drops the "resource." part from column names.
        entry.columns = entry.columns.str.replace('resource.', '')
        try:
            # check if this id already exists
            with engine.connect() as connection:
                exists = bool(connection.execute(
                    text(f'SELECT id FROM "{fhir_object["table"]}" WHERE id = :id'),
                    {'id': fhir_object["data"]["id"]}
                ).scalar())
        except (ProgrammingError, OperationalError):
            # allow tables not to be defined, if it doesn't exist here it gets created below
            exists = False
        if exists:
            print(
                f"ID {fhir_object['data']['id']} "
                f"already exists in table {fhir_object['table']}, skipping.")
            return
        
        # put this section of the data into the database
        # this is a super easy, perhaps somewhat hacky way, to create tables on the fly.
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        # in a production environment it would be more sensible to
        # create defined schemas for the tables, but for a simple ETL app
        # like this it works and it's also fast to set up
        entry.to_sql(
            name=fhir_object["table"],
            con=engine,
            if_exists="append",
            index=False
        )
