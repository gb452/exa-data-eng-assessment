"""
Tests for loading raw FHIR data into fhir.resources objects
"""

import pytest
from fhir.resources.R4B.patient import Patient
from pydantic import ValidationError

from pipeline.loader import load_json


def test_good_data(load_json_fixture):
    """
    Test that when valid FHIR data is sent to load_json, a fhir.resources object is returned.
    """
    test_data = load_json_fixture("fhir_json/patient.json")

    expected_object = Patient.model_validate(test_data)

    assert expected_object == load_json(test_data)


def test_invalid_resource_type_string(load_json_fixture):
    """
    Test an appropriate message is logged when the resourceType key is missing
    """
    test_data = load_json_fixture("fhir_json/patient.json")
    del test_data["resourceType"]

    test_data["TypeResource"] = "foo"

    with pytest.raises(KeyError):
        load_json(test_data)


def test_invalid_resource_type_value(load_json_fixture):
    """
    Test an appropriate message is logged when the resourceType value is invalid
    """
    test_data = load_json_fixture("fhir_json/patient.json")
    test_data["resourceType"] = "bar"

    with pytest.raises(KeyError):
        load_json(test_data)


def test_invalid_fhir_data(load_json_fixture):
    """
    Test an appropriate message is logged when the FHIR data contains unexpected values
    """
    test_data = load_json_fixture("fhir_json/patient.json")
    test_data["anotherValue"] = "baz"

    with pytest.raises(ValidationError):
        load_json(test_data)
