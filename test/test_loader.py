
from fhir.resources.R4B.patient import Patient

from pipeline.loader import load_json


def test_good_data(load_json_fixture):

    test_data = load_json_fixture("fhir_json/patient.json")

    expected_object = Patient.model_validate(test_data)

    assert expected_object == load_json(test_data)

    pass


def test_invalid_resource_type_string(load_json_fixture, capsys):

    test_data = load_json_fixture("fhir_json/patient.json")
    del test_data["resourceType"]

    test_data["TypeResource"] = "foo"

    load_json(test_data)

    expected_message = "Failed to load data into FHIR Resource: 'resourceType', KeyError"

    captured_output = capsys.readouterr()

    assert expected_message in captured_output.out


def test_invalid_resource_type_value(load_json_fixture, capsys):

    test_data = load_json_fixture("fhir_json/patient.json")
    test_data["resourceType"] = "bar"

    load_json(test_data)

    expected_message = "Failed to load data into FHIR Resource: 'bar', KeyError"

    captured_output = capsys.readouterr()

    assert expected_message in captured_output.out


def test_invalid_fhir_data(load_json_fixture, capsys):

    test_data = load_json_fixture("fhir_json/patient.json")
    test_data["anotherValue"] = "baz"

    load_json(test_data)

    expected_message = "Failed to load data into FHIR Resource: 1 validation error for Patient"

    captured_output = capsys.readouterr()

    assert expected_message in captured_output.out