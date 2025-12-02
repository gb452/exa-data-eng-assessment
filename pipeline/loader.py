"""
Utility to load raw JSON data into the appropriate fhir.resources object

Use a mapping so we can take the resourceType field from the JSON to know what object to use
"""

from fhir_core.fhirabstractmodel import FHIRAbstractModel
import importlib
from typing import Any

from constants import RESOURCE_TYPES

# Various bits below are AI generated and then adjusted by me over time (I marked where it ends)


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
    # The data provided is version R4B.
    module = importlib.import_module(f"fhir.resources.R4B.{resource_name.lower()}")
    # get the object from the module. for example, fhir.resources.patient contains the module Patient
    # the mapping in resource_types above is used for this
    return getattr(module, resource_name)

# finally, create a reusable mapping containing all of the modules we need to process the example data
IMPORT_MAP = {name: _load_resource_class(name) for name in RESOURCE_TYPES}
# this is the end of the AI code


def load_json(json_entry: dict[str, Any]) -> dict[str, str]:
    """
    Given a raw JSON entry from a fhir file, load it into a fhir.resources object.

    Don't expect any errors, as start.py will handle these and cancel processing if so.

    :param json_entry: JSON entry from the fhir file.
    :return: A fhir.resources object representing the data.
    """
    # find our resource type
    resource_type = json_entry["resourceType"]
    # load our raw data into the fhir.resources class to validate it
    loaded_resource = IMPORT_MAP[resource_type].model_validate(json_entry)
    return loaded_resource
