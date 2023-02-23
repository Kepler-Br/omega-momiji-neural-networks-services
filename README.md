### Text generator

#### A list of environment variables used by program

| Key               | Required | Type    | Possible values                               | Default |
|-------------------|----------|---------|-----------------------------------------------|---------|
| SERVER_MODEL_PATH | Yes      | String  | File system or hugging face path              |         |
| SERVER_USE_STUB   | No       | Boolean | TRUE, true, 1, True, **Any string as False**  | False   |
| SERVER_USE_CPU    | No       | Boolean | TRUE, true, 1, True, **Any string as False**  | False   |
| SERVER_PORT       | No       | Integer | A valid port number                           | 8080    |
| SERVER_HOST       | No       | String  | A valid IPv4 address                          | 0.0.0.0 |
| SERVER_WORKERS    | No       | Integer | 1>                                            | 2       |
| SERVER_LOG_LEVEL  | No       | String  | NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO    |
