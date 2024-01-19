# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/api-db-prototype/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                 |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/app.py                                           |       20 |        6 |     70% |15-18, 26-27, 31 |
| src/cloud\_services.py                               |       58 |       23 |     60% |15, 26-27, 60-65, 73-74, 79-80, 85-86, 91-101, 113, 136-137 |
| src/config.py                                        |       29 |        3 |     90% |49, 61, 69 |
| src/controllers/\_\_init\_\_.py                      |        0 |        0 |    100% |           |
| src/controllers/auth.py                              |       20 |        0 |    100% |           |
| src/controllers/helper.py                            |       80 |       11 |     86% |     41-53 |
| src/controllers/models.py                            |      114 |       10 |     91% |79, 81, 108-109, 135-136, 152, 158-162 |
| src/controllers/users/auth.py                        |       25 |        2 |     92% |     27-28 |
| src/controllers/users/create.py                      |       22 |        0 |    100% |           |
| src/controllers/users/delete.py                      |       19 |        1 |     95% |        19 |
| src/controllers/users/get.py                         |       16 |        2 |     88% |    18, 21 |
| src/controllers/users/list.py                        |       42 |        7 |     83% |35, 40, 42, 48-51 |
| src/controllers/users/update.py                      |       24 |        2 |     92% |    21, 26 |
| src/controllers/version.py                           |        7 |        4 |     43% |      8-11 |
| src/db/conn.py                                       |       53 |        0 |    100% |           |
| src/db/models.py                                     |       68 |        6 |     91% |31, 77, 111, 130, 137, 154 |
| src/flask\_server/\_\_init\_\_.py                    |        0 |        0 |    100% |           |
| src/journaling.py                                    |       52 |        4 |     92% | 36, 97-99 |
| src/jwt\_token.py                                    |       49 |        0 |    100% |           |
| src/openapi\_server/api\_app.py                      |        5 |        0 |    100% |           |
| src/openapi\_server/apikey\_fake.py                  |        2 |        0 |    100% |           |
| src/openapi\_server/controllers/users\_controller.py |       36 |        0 |    100% |           |
| src/openapi\_server/encoder.py                       |       17 |        0 |    100% |           |
| src/openapi\_server/models/\_\_init\_\_.py           |       10 |        0 |    100% |           |
| src/openapi\_server/models/base\_model\_.py          |       31 |       16 |     48% |23, 30-52, 59, 63, 67, 71 |
| src/openapi\_server/models/error.py                  |       19 |        6 |     68% |24-28, 39, 50, 62 |
| src/openapi\_server/models/new\_user.py              |       12 |        3 |     75% | 20-22, 33 |
| src/openapi\_server/models/new\_user\_response.py    |       21 |        8 |     62% |24-28, 39, 50, 61-64 |
| src/openapi\_server/models/token.py                  |       19 |        6 |     68% |24-28, 39, 50, 62 |
| src/openapi\_server/models/update\_user.py           |       34 |       12 |     65% |29-35, 46, 56, 67, 77, 88, 98, 109 |
| src/openapi\_server/models/user.py                   |       42 |       15 |     64% |32-39, 50, 60, 71, 81, 92, 102, 113, 123, 134 |
| src/openapi\_server/models/user\_credentials.py      |       26 |        0 |    100% |           |
| src/openapi\_server/models/user\_group.py            |       16 |        3 |     81% | 27-29, 40 |
| src/openapi\_server/models/user\_short.py            |       34 |       12 |     65% |29-35, 46, 56, 67, 77, 88, 98, 109 |
| src/openapi\_server/util.py                          |       54 |        6 |     89% |21, 57, 72-73, 90-91 |
| src/password\_hash.py                                |        5 |        0 |    100% |           |
| src/pretty\_ns.py                                    |       34 |        7 |     79% |46, 51, 81-84, 88-90 |
| src/settings.py                                      |      123 |       17 |     86% |93, 98, 110, 178-181, 186, 194-200, 205, 214 |
| src/version.py                                       |        8 |        1 |     88% |        17 |
|                                            **TOTAL** | **1246** |  **193** | **85%** |           |


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