# test/test_extract.py

"""
Tests for extract.py

These are basic tests that will verify a provided fhir.resource object
is transformed into the expected JSON output. Further validation
and error handling is handled in test_loader.py
"""

from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.encounter import Encounter
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.claim import Claim
from fhir.resources.R4B.procedure import Procedure
from fhir.resources.R4B.immunization import Immunization
from fhir.resources.R4B.medicationrequest import MedicationRequest
from fhir.resources.R4B.medication import Medication

from pipeline.extract import (
    patient,
    encounter,
    condition,
    claim,
    procedure,
    immunization,
    medicationrequest,
    medication
)


def test_load_patient(load_json_fixture):
    """Test that data for a Patient can be loaded"""
    test_patient = Patient.model_validate(load_json_fixture("fhir_json/patient.json"))
    expected_patient = load_json_fixture("transformed_json/patient.json")
    
    assert expected_patient == patient(test_patient)


def test_load_encounter(load_json_fixture):
    """Test that data for an Encounter can be loaded"""
    test_encounter = Encounter.model_validate(load_json_fixture("fhir_json/encounter.json"))
    expected_encounter = load_json_fixture("transformed_json/encounter.json")
    
    assert expected_encounter == encounter(test_encounter)


def test_load_condition(load_json_fixture):
    """Test that data for a Condition can be loaded"""
    test_condition = Condition.model_validate(load_json_fixture("fhir_json/condition.json"))
    expected_condition = load_json_fixture("transformed_json/condition.json")
    
    assert expected_condition == condition(test_condition)


def test_load_claim(load_json_fixture):
    """Test that data for a Claim can be loaded"""
    test_claim = Claim.model_validate(load_json_fixture("fhir_json/claim.json"))
    expected_claim = load_json_fixture("transformed_json/claim.json")
    
    assert expected_claim == claim(test_claim)


def test_load_procedure(load_json_fixture):
    """Test that data for a Procedure can be loaded"""
    test_procedure = Procedure.model_validate(load_json_fixture("fhir_json/procedure.json"))
    expected_procedure = load_json_fixture("transformed_json/procedure.json")
    
    assert expected_procedure == procedure(test_procedure)


def test_load_immunization(load_json_fixture):
    """Test that data for an Immunization can be loaded"""
    test_immunization = Immunization.model_validate(load_json_fixture("fhir_json/immunization.json"))
    expected_immunization = load_json_fixture("transformed_json/immunization.json")
    
    assert expected_immunization == immunization(test_immunization)


def test_load_medicationrequest(load_json_fixture):
    """Test that data for a MedicationRequest can be loaded"""
    test_medicationrequest = MedicationRequest.model_validate(load_json_fixture("fhir_json/medicationrequest.json"))
    expected_medicationrequest = load_json_fixture("transformed_json/medicationrequest.json")
    
    assert expected_medicationrequest == medicationrequest(test_medicationrequest)


def test_load_medication(load_json_fixture):
    """Test that data for a Medication can be loaded"""
    test_medication = Medication.model_validate(load_json_fixture("fhir_json/medication.json"))
    expected_medication = load_json_fixture("transformed_json/medication.json")
    
    assert expected_medication == medication(test_medication)