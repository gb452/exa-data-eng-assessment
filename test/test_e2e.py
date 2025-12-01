"""
End to end test of processing one file
"""
from pipeline.start import start


def test_e2e(capsys, monkeypatch, test_db_engine):
    """A simple end to end test to verify that the pipeline outputs the correct logs"""
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    monkeypatch.setattr("pipeline.database.get_db_engine", test_db_engine)
    # patch out os.makedirs
    monkeypatch.setattr("pipeline.start.makedirs", lambda x, exist_ok: None)
    # patch out shutil.move
    monkeypatch.setattr("shutil.move", lambda x, y: None)
    # patch os.listdir to make it use our test file
    monkeypatch.setattr("pipeline.start.listdir", lambda x: ["test/test_files/e2e/full_file.json"])
    # patch os.path.join to use the test patch
    monkeypatch.setattr("pipeline.start.join", lambda x, y: "test/test_files/e2e/full_file.json")

    # run the test
    start(test=True)

    # verify that logs show the processing was successful
    expected_message = "Successfully processed file test/test_files/e2e/full_file.json!"
    captured_output = capsys.readouterr()
    assert expected_message in captured_output.out
