"""
Utility code for using and accessing the database
"""

from functools import lru_cache

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

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
    db_host = os.getenv('DATABASE_HOSTNAME', "localhost")
    db_port = os.getenv('DATABASE_PORT', "5433")
    db_name = os.getenv('DATABASE_NAME', "patientdata")
    db_user = os.getenv('DATABASE_USERNAME', "postgres")
    db_pass = os.getenv('DATABASE_PASSWORD', "mypassword")

    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(db_url)
    return engine

def send_object(fhir_object):
    """
    Upload JSON representing the FHIR object to the database
    """

    print(fhir_object)
    if fhir_object["data"]:
        entry = json_normalize(fhir_object["data"])
        # Below line is AI generated - drops the "resource." part from column names.
        entry.columns = entry.columns.str.replace('^resource\.', '', regex=True)
        
        # put this section of the data into the database
        # this is a super easy, perhaps somewhat hacky way, to create tables on the fly.
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        # in a production environment it would be more sensible to create defined schemas for the tables,
        # but for a simple ETL app like this it works.
        entry.to_sql(name=fhir_object["table"], con=get_db_engine(), if_exists="append", index=False)
