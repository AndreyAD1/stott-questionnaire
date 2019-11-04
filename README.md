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

1. Set an environment variable `FLASK_APP`.

    On Linux:
    ```bash
    (venv) $ export FLASK_APP=questionnaire.py
    ```
    On Windows:
    ```bash
    (venv) > set FLASK_APP=questionnaire.py
    ```

2. Create a database and set an environment variable `DATABASE_URL`
(see examples of database URLs [here](https://docs.sqlalchemy.org/en/latest/core/engines.html)). 
By default, the database url is
`postgresql://stott:stott@127.0.0.1/stott_questionnaire`
(username: 'stott', password: 'stott', database name: 'stott_questionnaire'.
    On Linux:
    ```bash
    (venv) $ export DATABASE_URL=some_url
    ```
    On Windows:
    ```bash
    (venv) > set DATABASE_URL=some_url
    ```

3. Create the database migration script:
    ```bash
    $ flask db migrate 
    ```
   You may encounter an import problem with module Tkinter. In that case you
   should install the system package `tk-devel` and rebuild Python.
4. Add tables to the database:
    ```bash
    $ flask db upgrade
    ```
4. Run the server on `http://127.0.0.1:5000/`:
    ```bash
    $ flask run
    ```
