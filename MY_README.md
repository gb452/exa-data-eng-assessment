# Temporary readme to keep track of progress

## The Task
An external system / supplier is sending patient data to our platform using the FHIR standard. Our analytics teams find this format difficult to work with when creating dashboards and visualizations. You are required to tranform these FHIR messages into a more workable format preferably in a tabular format. Include any documentation / commentary you deem necessary.

- takes in fhir data
- transforms to a workable tabular format
- loads them into postgres



- **Functionality**: Is the solution correct? Does it run in a decent amount of time? How well thought and architected is the solution?
    - meets the basic requirements
    - runs in a reasonable amount of time
    - codebase is split into separate files for each section of the app etc
- **Good Practices**: Does the code follow standard practices for the language and framework used? Take into account reusability, names, function length, structure, how crendentials are handled, etc.
    - linted
    - functions do one task
    - credentials - move into a .env file?
    - can send more data in without having to restart the system
- **Testing**: Unit and integration tests.
    - need to do these!
- **Execution environment**: Container, Virtual Environment, Dependency Management, Isolation, Ease of transition into a production environment etc.
    - docker composed and containerised
    - requirements.txt for dependencies
- **Documentation**: How to install and run the solution? How to see and use the results? What is the architecture? Any next steps?
    - do readme writeup for how to run etc
