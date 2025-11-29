"""
Utility to load raw JSON data into the appropriate fhir.resources object

Use a mapping so we can take the resourceType field from the JSON to know what object to use
"""

from fhir_core.fhirabstractmodel import FHIRAbstractModel
import importlib
from typing import Any

from extract import patient, encounter, condition, diagnosticreport, documentreference, claim, explanationofbenefit, observation, \
    procedure, careteam, careplan, immunization, medicationrequest, imagingstudy, medication, medicationadministraction, provenance

# The code below is partially AI generated

# A mapping of resource type to extraction function
# The keys in this are also used to import all the necessary modules in
# the _load_resource_class function so that there aren't a load of
# ugly imports at the top of this file
RESOURCE_TYPES = {
    "Patient": patient,
    "Encounter": encounter,
    "Condition": condition,
    "DiagnosticReport": diagnosticreport,
    "DocumentReference": documentreference,
    "Claim": claim,
    "ExplanationOfBenefit": explanationofbenefit,
    "Observation": observation,
    "Procedure": procedure,
    "CareTeam": careteam,
    "CarePlan": careplan,
    "Immunization": immunization,
    "MedicationRequest": medicationrequest,
    "ImagingStudy": imagingstudy,
    "Medication": medication,
    "MedicationAdministration": medicationadministraction,
    "Provenance": provenance
}


def _load_resource_class(resource_name: str) -> FHIRAbstractModel:
    """
    Load the relevant fhir.resources object, for use in a mapping of the string name to the object.

    This is done as otherwise each one will have to be imported individually and the mapping made by hand

    Essentially, this is neater and takes up less space.

    Type hint for FHIRAbstractModel as this covers all of our possible resource types.

    :param resource_name: The name of the resource pulled from the JSON data
    :return: fhir.resources object for this resource name
    """
    # import the module, for example fhir.resources.patient
    # we need to specify fhir version R4B as the package defaults to R5.
    module = importlib.import_module(f"fhir.resources.R4B.{resource_name.lower()}")
    # get the object from the module. for example, fhir.resources.patient contains the module Patient
    # the mapping in resource_types above is used for this
    return getattr(module, resource_name)

# create a reusable mapping containing all of the modules we need to process the example data
RESOURCE_MAP = {name: _load_resource_class(name) for name in RESOURCE_TYPES}
# this is the end of the AI code

def load_and_transform_json(json_entry: dict[str, Any]):
    """
    Given a raw JSON entry from a fhir file, load it into a fhir.resources object and transform it into
    a usable dictionary of information.

    :param json_entry: JSON entry from the fhir file.
    :return: dict of values useful for this type.
    """

    try:
        # find our resource type
        resource_type = json_entry["resourceType"]
        # load our raw data into the fhir.resources class to validate it
        loaded_resource = RESOURCE_MAP[resource_type].model_validate(json_entry)
        # use the resource types dict to then send that object to the transformation function
        return RESOURCE_TYPES[resource_type](loaded_resource)
    except Exception as exc:
        print(f"Failed to load data into FHIR Resource: {exc}")
