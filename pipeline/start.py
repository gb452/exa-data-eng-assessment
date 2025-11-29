


import time
import json
import os
from shutil import move

import pandas as pd

from loader import RESOURCE_MAP, load_json_to_object
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
                fhir_objects.append(load_json_to_object(patient_data_entry["resource"]))
            patient = fhir_objects[0]

            print(patient.name[0].given[0])
            print(patient.name[0].family)
            # print(patient)

            df = pd.json_normalize(patient.dict())


            for col in list(df.columns):
                if isinstance(df[col][0], list):
                    df[col] = df[col].apply(json.dumps)
            print(df.columns)
            df.to_sql(name="Patient", con=get_db_engine(), if_exists="replace", index=False)
            # TODO will need to probably manually get things out of the model since it's not very good looking in the database.

                #     move(os.path.join(FILE_DIR, input_file), os.path.join(PROCESSED_FILE_DIR, input_file))
                # except Exception as exc:
                #     print(exc)
                #     move(os.path.join(FILE_DIR, input_file), os.path.join(FAILED_FILE_DIR, input_file))


if __name__ =="__main__":

    start()