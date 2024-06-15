## <center> FASTAPI</center>

- ### Pre-requirements

  1. Install python >= `3.10.0` first !!!

  2. Clone the repo

  3. Create .venv (python virtual environment) at same level as src folder

     > `python -m venv .venv`

     - for spesific python version:
       > `py -3.10 -m venv .venv`

  4. Instal pipenv in your python virtual environment

     $ `pip install pipenv`

     - documentation for pipenv
       [pipenv doc](https://pipenv.pypa.io/en/latest/basics/)

  5. Install from Pipfile, if there is one
     > `pipenv install`
  6. Add a package to your new project
     > `pipenv install <package>` > `This will create a Pipfile if one doesn’t exist. If one does exist, it will automatically be edited with the new package you provided.`
  7. Activate the Pipenv shell:
     > `pipenv shell` > `Addtional for pipenv, not need to run the command`

- ### DB migration using Alembic

  - Check current version:

    > `alembic current`

  - Auto make migration:

    > `alembic revision --autogenerate -m "[ticket_number]"`

  - Online migration (for dev)

    > `alembic upgrade head`

    > `alembic upgrade <revision>`

    > `alembic downgrade <revision>`

  - Offline migration (for qat, prod)

  - Generate script from all revision:

    > `alembic upgrade head --sql`

  - Generate script from start_revision to end_revision :

    > `alembic upgrade <start_revision>:<end_revision> --sql`
