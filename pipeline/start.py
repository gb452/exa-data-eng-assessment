import time
import json
import os
from shutil import move

import pandas as pd

# from extract import extract_patient 
from loader import load_json_to_object
from constants import FILE_DIR, PROCESSED_FILE_DIR, FAILED_FILE_DIR

from dbconn import get_db_engine


# filename = "../data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json"

# with open(filename, "r") as patient_file:
#     json_data = json.load(patient_file)

# the_patient = Patient.model_validate(json_data["entry"][0]["resource"])
# print(the_patient.managingOrganization)


def start():
    """
    Main function for running the pipeline.

    Continually read files from the input directory, load them in, transform them to usable data and send then to the
    Postgres database.

    Once a file has been ingested, move then to a subfolder within the input directory called "finished".
    """

    os.makedirs(FILE_DIR, exist_ok=True)
    os.makedirs(PROCESSED_FILE_DIR, exist_ok=True)
    os.makedirs(FAILED_FILE_DIR, exist_ok=True)

    # while True:

    if found_files := [f for f in os.listdir(FILE_DIR) if f.endswith('.json')]:
        for input_file in found_files:
            # try:
            with open(os.path.join(FILE_DIR, input_file), "r") as file_data:
                raw_json = json.load(file_data)

            fhir_objects = []

            # each fhir file has all of the data under the "entry" key.
            for patient_data_entry in raw_json["entry"]:
                if patient_data_entry["resource"]["resourceType"] == "Patient":
                    fhir_objects.append(load_json_to_object(patient_data_entry["resource"]))
            for fhir_object in fhir_objects:
                print(fhir_object)
                dataframe = pd.json_normalize(fhir_object)
                # Below line is AI generated - drops the "resource." part from column names.
                dataframe.columns = dataframe.columns.str.replace('^resource\.', '', regex=True)
                
                # put this section of the data into the database
                dataframe.to_sql(name="Patient", con=get_db_engine(), if_exists="append", index=False)


if __name__ =="__main__":

    start()