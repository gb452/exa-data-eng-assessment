"""
Functions to extract data from each type of fhir.resources model.

We can load the data into a model to validate it is in a correct format
for FHIR data, but it's easier to pull out relevant data from each model.
The data is nested if left as is so it can't be transferred directly to
a database.

The other benefit of using fhir.resources is that we don't have to
directly access the JSON.
"""

from datetime import datetime

from fhir.resources.R4B.claim import Claim

def patient(patient):
    """
    Extract data from a Patient model to get it ready for database entry.
    """

    return_dict = {}

    # basic entries for these values that will be overridden if they exist
    return_dict["social_security_number"] ="N/A"
    return_dict["drivers_license"] ="N/A"
    return_dict["passport_number"] ="N/A"

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
    return_dict["birth_date"] = datetime.strftime(patient.birthDate, "%Y-%m-%d %H:%M:%S")
    try:
        return_dict["deceased_date"] = datetime.strftime(patient.deceasedDateTime, "%Y-%m-%d %H:%M:%S")
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

def encounter(encounter):

    return_dict = {}
    return_dict["encounter_id"] = encounter.id
    return_dict["medical_record_number"] = encounter.subject.reference.split(":")[-1]
    return_dict["status"] = encounter.status
    return_dict["type"] = encounter.type[0].coding[0].display
    return_dict["start_date"] = datetime.strftime(encounter.period.start, "%Y-%m-%d %H:%M:%S")
    return_dict["end_date"] = datetime.strftime(encounter.period.end, "%Y-%m-%d %H:%M:%S")
    return_dict["subject"] = encounter.subject.display
    return_dict["participant"] = encounter.participant[0].individual.display
    return_dict["location"] = encounter.location[0].location.display
    return_dict["service_provider"] = encounter.serviceProvider.display

    return return_dict

def condition(condition):

    return_dict = {}


    return_dict["condition_id"] = condition.id
    return_dict["medical_record_number"] = condition.subject.reference.split(":")[-1]
    return_dict["encounter"] = condition.encounter.reference.split(":")[-1]

    return_dict["clinical_status"] = condition.clinicalStatus.coding[0].code
    return_dict["verification_status"] = condition.verificationStatus.coding[0].code
    return_dict["category"] = condition.category[0].coding[0].display
    return_dict["onset_date"] = datetime.strftime(condition.onsetDateTime, "%Y-%m-%d %H:%M:%S")
    # not every condition has been abated
    try:
        return_dict["abatement_date"] = datetime.strftime(condition.abatementDateTime, "%Y-%m-%d %H:%M:%S")
    except (KeyError, TypeError):
        return_dict["abatement_date"] = None
    return_dict["condition_information"] = condition.code.text

    return return_dict

def claim(claim: Claim):
    """
    Transform claim data into a usable format
    """

    return_dict = {}

    return_dict["claim_id"] = claim.id
    return_dict["medical_record_number"] = claim.patient.reference.split(":")[-1]
    return_dict["encounter_id"] = claim.item[0].encounter[0].reference.split(":")[-1]
    # not every claim has a condition associated with it, for example a general exam or assessment.
    try:
        return_dict["condition_id"] = claim.diagnosis[0].diagnosisReference.reference.split(":")[-1]
    except (KeyError, TypeError):
        return_dict["condition_id"] = None
    return_dict["status"] = claim.status
    return_dict["billable_period_start"] = datetime.strftime(claim.billablePeriod.start, "%Y-%m-%d %H:%M:%S")
    return_dict["billable_period_end"] = datetime.strftime(claim.billablePeriod.end, "%Y-%m-%d %H:%M:%S")
    return_dict["provider"] = claim.provider.display
    return_dict["priority"] = claim.priority.coding[0].code
    return_dict["insurance_coverage"] = claim.insurance[0].coverage.display
    return_dict["total_cost"] = f"{(claim.total.value):.2f}{claim.total.currency}"
    
    return return_dict

def procedure(procedure):
    
    return_dict = {}

    return_dict["procedure_id"] = procedure.id
    return_dict["medical_record_number"] = procedure.subject.reference.split(":")[-1]
    return_dict["encounter_id"] = procedure.encounter.reference.split(":")[-1]
    return_dict["status"] = procedure.status
    return_dict["performed_period_start"] = datetime.strftime(procedure.performedPeriod.start, "%Y-%m-%d %H:%M:%S")
    return_dict["performed_period_end"] = datetime.strftime(procedure.performedPeriod.end, "%Y-%m-%d %H:%M:%S")
    return_dict["location"] = procedure.location.display

    return return_dict

def immunization(immunization):
    
    return_dict = {}

    return_dict["immunization_id"] = immunization.id
    return_dict["medical_record_number"] = immunization.patient.reference.split(":")[-1]
    return_dict["encounter_id"] = immunization.encounter.reference.split(":")[-1]
    return_dict["vaccine_code"] = immunization.vaccineCode.coding[0].code
    return_dict["vaccine_type"] = immunization.vaccineCode.coding[0].display
    return_dict["occurrence_date"] = datetime.strftime(immunization.occurrenceDateTime, "%Y-%m-%d %H:%M:%S")
    return_dict["location"] = immunization.location.display

    return return_dict

def medicationrequest(medicationrequest):
    
    return_dict = {}

    return_dict["medication_request_id"] = medicationrequest.id
    return_dict["medical_record_number"] = medicationrequest.subject.reference.split(":")[-1]
    return_dict["encounter_id"] = medicationrequest.encounter.reference.split(":")[-1]
    # not every request has a reason in there, for example ibuprofen does not appear to require one
    try:
        return_dict["condition_id"] = medicationrequest.reasonReference[0].reference.split(":")[-1]
    except (KeyError, TypeError, ValueError, AttributeError):
        return_dict["condition_id"] = None
    return_dict["status"] = medicationrequest.status
    return_dict["intent"] = medicationrequest.intent
    # not every medication request records the medication in there, sometimes it's listed as a separate Medication entry
    try:
        return_dict["medication_code"] = medicationrequest.medicationCodeableConcept.coding[0].code
        return_dict["medication_name"] = medicationrequest.medicationCodeableConcept.coding[0].display
        return_dict["medication_reference_id"] = None
    except (KeyError, ValueError, AttributeError) as exc:
        print(exc)
        print("^")
        return_dict["medication_reference_id"] = medicationrequest.medicationReference.reference.split(":")[-1]
        return_dict["medication_code"] = None
        return_dict["medication_name"] = None

    return_dict["requester"] = medicationrequest.requester.display

    return return_dict

def medication(medication):
    
    return_dict = {}

    return_dict["medication_id"] = medication.id
    return_dict["medication_status"] = medication.status
    return_dict["medication_code"] = medication.code.coding[0].code
    return_dict["medication_name"] = medication.code.coding[0].display

    return return_dict

