"""
Functions to extract data from each type of fhir.resources model.

We can load the data into a model to validate it is in a correct format
for FHIR data, but it's easier to pull out relevant data from each model.
The data is nested if left as is so it can't be transferred directly to
a database.
"""

import json
import time

from datetime import datetime

from fhir.resources.R4B.patient import Patient

def patient(patient: Patient):
    """
    Extract data from a Patient model to get it ready for database entry.
    """

    return_dict = {}

    # extract basic data
    # This section is AI generated - go through identifier section
    # to get the medical record number, social security, drivers licence
    # and passport numbers.
    for identifier in patient.identifier or []:
        if identifier.type and identifier.type.coding:
            for coding in identifier.type.coding:
                if coding.code == 'MR':  # Medical Record Number
                    return_dict["medical_record_number"] = identifier.value
                elif coding.code == 'SS':  # Social Security Number
                    return_dict["social_security_number"] = identifier.value
                elif coding.code == 'DL':  # Driver's License
                    return_dict["drivers_license"] = identifier.value
                elif coding.code == 'PPN':  # Passport Number
                    return_dict["passport_number"] = identifier.value

    # extract name data
    return_dict["given_name"] = patient.name[0].given[0]
    return_dict["family_name"] = patient.name[0].family

    # extract address data
    return_dict["house"] = patient.address[0].line[0]
    return_dict["city"] = patient.address[0].city
    return_dict["state"] = patient.address[0].state
    return_dict["country"] = patient.address[0].country

    # birth/death
    return_dict["birth_date"] = datetime.strftime(patient.birthDate, "%Y-%m-%d")
    try:
        return_dict["deceased_date"] = datetime.strftime(patient.deceasedDateTime, "%Y-%m-%d")
        return_dict["deceased"] = True
    except TypeError:
        return_dict["deceased_date"] = None
        return_dict["deceased"] = False

    # miscellaneous
    return_dict["gender"] = patient.gender
    return_dict["spoken_language"] = patient.communication[0].language.text
    return_dict["phone_number"] = patient.telecom[0].value
    return_dict["marital_status"] = patient.maritalStatus.coding[0].code

    return return_dict


# TODO - are all these actually needed? Do we want everything from the data or just the essentials?
def encounter():
    pass

def condition():  # want
    pass

def diagnosticreport():
    pass

def documentreference():
    pass

def claim():  # want
    pass

def explanationofbenefit():
    pass

def observation():  # want?
    pass

def procedure():  # want
    pass

def careteam():
    pass

def careplan():
    pass

def immunization():  # want
    pass

def medicationrequest():
    pass

def imagingstudy():
    pass

def medication():  # want
    pass

def medicationadministraction():
    pass

def provenance():
    pass