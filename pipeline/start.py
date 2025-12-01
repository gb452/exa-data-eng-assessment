import time
import json
import os
from shutil import move


# from extract import extract_patient 
from constants import RESOURCE_TYPES
from loader import load_json
from extract import transform_json
from database import send_object

FILE_DIR = "./files"

PROCESSED_FILE_DIR = f"{FILE_DIR}/finished"

FAILED_FILE_DIR = f"{FILE_DIR}/failed"


def start():
    """
    Main function for running the pipeline.

    Continually read files from the input directory, load them in, transform them to usable data and send
    them to the Postgres database.

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
                            loaded_data = load_json(patient_data_entry["resource"])
                            transformed_data = transform_json(patient_data_entry["resource"]["resourceType"], loaded_data)
                            fhir_objects.append({
                                "table": patient_data_entry["resource"]["resourceType"],
                                "data": transformed_data
                            })
                    for fhir_object in fhir_objects:
                        send_object(fhir_object)
                    move(os.path.join(FILE_DIR, input_file), os.path.join(PROCESSED_FILE_DIR, input_file))
                    print(f"Successfully processed file {input_file}!")
                except Exception as exc:
                    move(os.path.join(FILE_DIR, input_file), os.path.join(FAILED_FILE_DIR, input_file))
                    print(f"Processing error: {exc}")
        time.sleep(1)


if __name__ =="__main__":

    start()