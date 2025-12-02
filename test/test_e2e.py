"""
End to end test of processing one file
"""
from pipeline.start import start


def test_e2e(capsys, monkeypatch, test_db_engine, check_item_exists_in_table):
    """
    A simple end to end test to verify that the pipeline outputs the correct logs,
    and that an item exists in the Patient table with the expected ID.
    """
    # monkey patch the get_db_engine function with the test db engine
    # Do this so we use the in-memory db from the test_db_engine fixture
    monkeypatch.setattr("db.get_db_engine", test_db_engine)
    # patch out os.makedirs to do nothing
    # Do this and all the other ones below so that we don't create any files or directories while testing
    monkeypatch.setattr("pipeline.start.makedirs", lambda x, exist_ok: None)
    # patch out shutil.move to do nothing
    monkeypatch.setattr("shutil.move", lambda x, y: None)
    # patch os.listdir to return the test file
    monkeypatch.setattr("pipeline.start.listdir", lambda x: ["test/test_files/e2e/full_file.json"])
    # patch os.path.join to return the test file
    monkeypatch.setattr("pipeline.start.join", lambda x, y: "test/test_files/e2e/full_file.json")

    # run the test
    start(test=True)

    # verify that at least the Patient table was created, and the expected value exists inside it
    assert check_item_exists_in_table("Patient", "0f978b87-8054-e6d3-aa03-20e101ea37c0") == True

    # verify that logs show the processing was successful
    expected_message = "Successfully processed file test/test_files/e2e/full_file.json!"
    captured_output = capsys.readouterr()
    assert expected_message in captured_output.out
