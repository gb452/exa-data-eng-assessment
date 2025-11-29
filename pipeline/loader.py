"""
Utility to load raw JSON data into the appropriate fhir.resources object

Use a mapping so we can take the resourceType field from the JSON to know what object to use
"""

from fhir_core.fhirabstractmodel import FHIRAbstractModel
import importlib
from typing import Any

# The code below is AI generated
# Before this I imported each object from fhir.resources manually, and then set up a dict mapping for each.
# However that is really ugly and doing it this way does both the imports and the mapping in one go.
resource_types = [
    "Patient",
    "Encounter",
    "Condition",
    "DiagnosticReport",
    "DocumentReference",
    "Claim",
    "ExplanationOfBenefit",
    "Observation",
    "Procedure",
    "CareTeam",
    "CarePlan",
    "Immunization",
    "MedicationRequest",
    "ImagingStudy",
    "Medication",
    "MedicationAdministration",
    "Provenance",
]

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
RESOURCE_MAP = {name: _load_resource_class(name) for name in resource_types}
# this is the end of the AI code

def load_json_to_object(json_entry: dict[str, Any]):
    """
    Given a raw JSON entry from a fhir file, load it into a fhir.resources object.

    :param json_entry: JSON entry from the fhir file.
    :return: fhir.resources object for this entry type.
    """

    try:
        resource_type = json_entry["resourceType"]
        loaded_resource = RESOURCE_MAP[resource_type].model_validate(json_entry)
    except Exception as exc:
        print(f"Failed to load data into FHIR Resource: {exc}")
    return loaded_resource
