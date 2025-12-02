"""
Tests for database connectivity
"""

import pytest
from pipeline.db import send_object


@pytest.fixture(autouse=True)
def setup(monkeypatch, test_db_engine):
    """
    Setup function that runs before each database test
    """
    # Monkey patch the get_db_engine function with the test db engine
    # Do this for every test so we use the in-memory db from the test_db_engine fixture
    monkeypatch.setattr("pipeline.db.get_db_engine", test_db_engine)


def test_send_to_database_new_item_new_table(load_json_fixture, check_table_exists, check_item_exists_in_table):
    """
    Test that a new item can be sent to the database, and a new table is created for it.
    """
    # send new item
    transformed_data = load_json_fixture("transformed_json/medication.json")
    data_to_send ={
        "table": "Medication",
        "data": transformed_data
    }
    send_object(data_to_send)

    # test table created with correct name
    assert check_table_exists("Medication") == True

    # test item is in table
    assert check_item_exists_in_table("Medication", transformed_data["id"]) == True


def test_send_two_to_database(load_json_fixture, check_item_exists_in_table):
    """
    Test that when two items are sent to an empty database, two items exist in the resulting table.
    """
    # send one item
    transformed_data = load_json_fixture("transformed_json/medication.json")
    data_to_send = {
        "table": "Medication",
        "data": transformed_data
    }
    data_to_send["data"]["id"] = "original_id"
    send_object(data_to_send)

    # send another item
    data_to_send["data"]["id"] = "new_id"
    send_object(data_to_send)

    # test first item is in table
    assert check_item_exists_in_table("Medication", "original_id") == True
    # test second item is in table
    assert check_item_exists_in_table("Medication", "new_id") == True


def test_already_exists(load_json_fixture, capsys):
    """
    Test that if an item already exists (based on id value), it is not added to the table
    """
    # send one item
    transformed_data = load_json_fixture("transformed_json/medication.json")
    data_to_send = {
        "table": "Medication",
        "data": transformed_data
    }
    data_to_send["data"]["id"] = "foobar"
    send_object(data_to_send)

    # send the same item again
    send_object(data_to_send)

    # check response has correct string
    expected_message = "ID foobar already exists in table Medication, skipping."
    captured_output = capsys.readouterr()
    assert expected_message in captured_output.out
