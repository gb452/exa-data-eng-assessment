# Data processing tool

Thank you for taking the time to look at my submission for the tech test.

This solution meets the requirements of the outline in the original README:

- Takes in FHIR data
- Transforms it to a usable format
- Uploads it to a data storage layer
- Containerised with docker-compose

This solution also verifies that the FHIR data being entered is valid data.

Tests have also been written for each part of the pipeline. These are detailed further down.

# Running

To get right in and run the pipeline, run `docker compose up --build` from the main directory of this repo.

Once everything is built, you can send files to be processed by placing them into the `pipeline/files` directory.
Don't put them inside the `failed` or `finished` subdirectories, as this is where files that have been processed are placed.

The pipeline will automatically ingest new files from this directory, and move them to one of those subfolders once finished.

To view just the logs for the processing service, use `docker compose logs data_processing`.

The data storage layer is Postgres, so you can use any tool like pgAdmin4 to view the database in a GUI. The server will be mapped to run on localhost:5433 by docker. Connectivity information can be found in the `.env` variables file. (note that the port in there is 5432 as that is used inside the docker container - you should still use 5433 when connecting outside of it)

# Tests

The tests are written with Pytest, so you can just run `pytest` from the main directory to run them.

There are 16 tests in total.

# Data validation, extraction, transformation and loading

This is some information about the technical approach for my solution.

As mentioned above my pipeline will also check you're sending valid FHIR data.

To do this I have used a library called `fhir.resources`.

This library translates the raw data into Pydantic models, which does the validation for me, and also makes it easier to pull out the relevant parts of the data.

Once the data is validated, it's pulled out of the model and transformed into a workable format.
This consists of a flat dictionary, and the values are different for each model.
You can see this in the `extract.py` file.

After the data has been transformed it can be loaded into the database.
To do this as simply as possible, the data is put into a pandas dataframe, which then lets me use the `to_sql` function in pandas to send this straight into the database and create any new tables on the fly.

There is some more discussion around that setup in the `db.py` file.
