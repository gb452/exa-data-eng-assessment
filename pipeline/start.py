import time
import json
import os
from shutil import move


# from extract import extract_patient 
from loader import load_and_transform_json, RESOURCE_TYPES
from constants import FILE_DIR, PROCESSED_FILE_DIR, FAILED_FILE_DIR

from database import send_object


# filename = "../data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json"

# with open(filename, "r") as patient_file:
#     json_data = json.load(patient_file)

# the_patient = Patient.model_validate(json_data["entry"][0]["resource"])
# print(the_patient.managingOrganization)


def start():
    """
    Main function for running the pipeline.

    Continually read files from the input directory, load them in, transform them to usable data and send them to the
    Postgres database.

    Once a file has been ingested, move then to a subfolder within the input directory called "finished".
    If it fails move it to a subfolder called "failed".
    """

    os.makedirs(FILE_DIR, exist_ok=True)
    os.makedirs(PROCESSED_FILE_DIR, exist_ok=True)
    os.makedirs(FAILED_FILE_DIR, exist_ok=True)

    # continue to loop forever so we can pick up any new files
    while True:
        if found_files := [f for f in os.listdir(FILE_DIR) if f.endswith('.json')]:
            # go through each file
            for input_file in found_files:
                try:
                    with open(os.path.join(FILE_DIR, input_file), "r") as file_data:
                        raw_json = json.load(file_data)

                    # represents the objects for this fhir file
                    fhir_objects = []

                    # each fhir file has all of the data under the "entry" key.
                    for patient_data_entry in raw_json["entry"]:
                        if patient_data_entry["resource"]["resourceType"] in RESOURCE_TYPES:
                            fhir_objects.append({
                                "table": patient_data_entry["resource"]["resourceType"],
                                "data": load_and_transform_json(patient_data_entry["resource"])
                            })
                    for fhir_object in fhir_objects:
                        send_object(fhir_object)
                    move(os.path.join(FILE_DIR, input_file), os.path.join(PROCESSED_FILE_DIR, input_file))
                except Exception as exc:
                    print(f"Processing error: {exc}")
                    move(os.path.join(FILE_DIR, input_file), os.path.join(FAILED_FILE_DIR, input_file))
        time.sleep(1)


if __name__ =="__main__":

    start()