## End-to-end web UI tests

Uses headless-browsers on selenuim grid server.

Use `setup.sh` to prepare for tests.
 
To start the server with the docker-compose.yaml and 
[allure](https://github.com/allure-framework/allure2) web-report generator
run in this folder:

    docker-compose up -d
    
Do not forget to start the server under test if you run it locally.
    
To run all tests:

    test.sh

Creates web-report on http://localhost:4040 .
