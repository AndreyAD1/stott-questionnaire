### Stott Questionnaire

This site provides psychological questionnaire helping 
to analyze social disadaptation of teenagers.

A static version of the site is here:
https://andreyad1.github.io/stott-questionnaire/static

### How To Install

Python v3.5 should be already installed. 
Afterwards use pip (or pip3 if there is a conflict with old Python 2 setup)
to install dependecies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember that it is recommended to use virtual environment for better isolation.

### Quick start

1. Using some PostgreSQL interface create PostgreSQL user with name 'stott'
 and password 'stott'. Create PostgreSQL database named 'stott_questionnaire';
2. Add project tables to the database 'stott_questionnaire':
    ```bash
    python database.py
    ```
3. Run the server on `http://127.0.0.1:5000/`:
    ```bash
    python server.py
    ```
