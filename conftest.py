"""
Pytest configurations and fixtures
"""

import pytest
import json
import sys

from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))

sys.path.insert(0, dirname(abspath(__file__)) + '/pipeline')

@pytest.fixture
def load_json_fixture():
    """Pytest fixture to load json from a file"""
    def _load(file_path):
        with open(f"{TEST_DIR}/test/test_files/{file_path}", "r") as f:
            return json.load(f)
        
    return _load