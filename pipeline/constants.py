"""
Constant values used in the pipeline
"""

# A mapping of resource type to extraction function
# This is used in extract.py
# The keys in this are also used to import all the necessary modules in
# the _load_resource_class function so that there aren't a load of
# ugly imports at the top of this file
RESOURCE_TYPES = [
    "Patient",
    "Encounter",
    "Condition",
    "Claim",
    "Procedure",
    "Immunization",
    "MedicationRequest",
    "Medication",
]