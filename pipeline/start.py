import time
import json
from os import listdir, makedirs
from os.path import join
from shutil import move


# from extract import extract_patient 
from constants import RESOURCE_TYPES
from loader import load_json
from extract import transform_json
from database import send_object

FILE_DIR = "./files"

PROCESSED_FILE_DIR = f"{FILE_DIR}/finished"

FAILED_FILE_DIR = f"{FILE_DIR}/failed"


def start(test=False):
    """
    Main function for running the pipeline.

    Continually read files from the input directory, load them in, transform them to usable data and send
    them to the Postgres database.

    Once a file has been ingested, move then to a subfolder within the input directory called "finished".
    If it fails move it to a subfolder called "failed".
    """

    makedirs(FILE_DIR, exist_ok=True)
    makedirs(PROCESSED_FILE_DIR, exist_ok=True)
    makedirs(FAILED_FILE_DIR, exist_ok=True)

    # continue to loop forever so we can pick up any new files
    while True:
        if found_files := [f for f in listdir(FILE_DIR) if f.endswith('.json')]:
            # go through each file
            for input_file in found_files:
                try:
                    with open(join(FILE_DIR, input_file), "r") as file_data:
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
                    move(join(FILE_DIR, input_file), join(PROCESSED_FILE_DIR, input_file))
                    print(f"Successfully processed file {input_file}!")
                except Exception as exc:
                    move(join(FILE_DIR, input_file), join(FAILED_FILE_DIR, input_file))
                    print(f"Processing error: {exc}")
        if test:
            break
        time.sleep(1)


if __name__ =="__main__":

    start()