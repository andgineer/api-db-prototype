# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/api-db-prototype/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                 |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/app.py                                           |       21 |        7 |     67% |15-19, 27-28, 32 |
| src/cloud\_services.py                               |       58 |       23 |     60% |15, 26-27, 60-65, 73-74, 79-80, 85-86, 91-101, 113, 136-137 |
| src/config.py                                        |       29 |        3 |     90% |50, 62, 70 |
| src/controllers/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| src/controllers/auth.py                              |       20 |        0 |    100% |           |
| src/controllers/helper.py                            |       80 |       11 |     86% |     42-54 |
| src/controllers/models.py                            |      114 |       10 |     91% |79, 81, 108-109, 135-136, 152, 158-162 |
| src/controllers/users/auth.py                        |       25 |        2 |     92% |     28-29 |
| src/controllers/users/create.py                      |       22 |        0 |    100% |           |
| src/controllers/users/delete.py                      |       19 |        1 |     95% |        19 |
| src/controllers/users/get.py                         |       16 |        2 |     88% |    19, 22 |
| src/controllers/users/list.py                        |       42 |        7 |     83% |35, 40, 42, 48-51 |
| src/controllers/users/update.py                      |       24 |        2 |     92% |    21, 26 |
| src/controllers/version.py                           |        7 |        4 |     43% |      9-12 |
| src/db/conn.py                                       |       53 |        0 |    100% |           |
| src/db/models.py                                     |       68 |        6 |     91% |31, 77, 111, 130, 137, 154 |
| src/flask\_server/\_\_init\_\_.py                    |        0 |        0 |    100% |           |
| src/journaling.py                                    |       52 |        4 |     92% |37, 98-100 |
| src/jwt\_token.py                                    |       49 |        0 |    100% |           |
| src/openapi\_server/api\_app.py                      |        3 |        0 |    100% |           |
| src/openapi\_server/apikey\_fake.py                  |        2 |        0 |    100% |           |
| src/openapi\_server/controllers/users\_controller.py |       39 |        0 |    100% |           |
| src/openapi\_server/encoder.py                       |       17 |        0 |    100% |           |
| src/openapi\_server/models/\_\_init\_\_.py           |        8 |        0 |    100% |           |
| src/openapi\_server/models/base\_model.py            |       30 |       16 |     47% |22, 29-49, 56, 60, 64, 68 |
| src/openapi\_server/models/error.py                  |       18 |        6 |     67% |21-29, 40, 51, 63 |
| src/openapi\_server/models/new\_user.py              |       12 |        0 |    100% |           |
| src/openapi\_server/models/new\_user\_response.py    |       20 |        8 |     60% |21-29, 40, 51, 62-65 |
| src/openapi\_server/models/token.py                  |       18 |        6 |     67% |21-29, 40, 51, 63 |
| src/openapi\_server/models/update\_user.py           |       34 |       12 |     65% |27-41, 52, 62, 73, 83, 94, 104, 115 |
| src/openapi\_server/models/user.py                   |       41 |       15 |     63% |29-46, 57, 67, 78, 88, 99, 109, 120, 130, 141 |
| src/openapi\_server/models/user\_credentials.py      |       25 |        0 |    100% |           |
| src/openapi\_server/models/user\_group.py            |       15 |        3 |     80% | 25-28, 40 |
| src/openapi\_server/models/user\_short.py            |       34 |       12 |     65% |27-41, 52, 62, 73, 83, 94, 104, 115 |
| src/openapi\_server/typing\_utils.py                 |       15 |        7 |     53% |      4-16 |
| src/openapi\_server/util.py                          |       59 |       10 |     83% |21, 47, 49, 58, 70, 75-76, 90, 95-96 |
| src/password\_hash.py                                |        5 |        0 |    100% |           |
| src/pretty\_ns.py                                    |       34 |        7 |     79% |47, 52, 82-85, 89-91 |
| src/settings.py                                      |      123 |       17 |     86% |93, 98, 110, 178-181, 186, 194-200, 205, 214 |
| src/version.py                                       |        8 |        1 |     88% |        18 |
|                                            **TOTAL** | **1259** |  **202** | **84%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/andgineer/api-db-prototype/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/api-db-prototype/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/andgineer/api-db-prototype/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/api-db-prototype/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fandgineer%2Fapi-db-prototype%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/api-db-prototype/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.