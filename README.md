# Event Manager Test #
This repository is a technical test.  
Packaging and dependencies of this project are managed with Poetry.

## Getting Started ##
Skip the <strong>environment setup</strong> if you want Poetry to handle the virtual environment, but make sure that the environment variable `POETRY_VIRTUALENVS_CREATE` is unset or True and that `virtualenvs.create` is true when running `poetry config --list`.

### Environment Setup ###
- Make sure you have `pyenv` installed by `pyenv -v`, if you need to install it follow the repo guide [pyenv install](https://github.com/pyenv/pyenv#installation);
- Make sure you have `pyenv virtualenv` installed by `pyenv virtualenvs`, if you need to install it follow the repo guide [pyenv virtualenv install](https://github.com/pyenv/pyenv-virtualenv#installation);
- Install any version of Python 3.11 through pyenv by `pyenv install 3.11`;
- Create a virtual environment with Python 3.11 by `pyenv virtualenv 3.11 <env_name>`;
- For ease of use, setup the local auto activation by `pyenv local <env_name>`, this will create a `.python-version` file already git-ignored;
- Create a `.env` file by following the `.env_sample` file.

### Project Setup ###
- Run `poetry install`;
- Run `poetry run migrate`;
- Run `poetry run createsuperuser` and follow the steps in order to create a super user that can access the admin console.

Now you will be able to run the server.

### Run the project ###
- `poetry run start`.

Now you will be able to fetch the API at [http://localhost:8000](http://localhost:8000).  
In order to test the API without any frontend app support, please use the Postman collection provided in the repository.
`event_manager_test.postman.json`

### Tests ###
- `poetry run pytest`.

### Contributing ###
Before any contributions make sure:
- the swagger is up-to-date, should be automatic, but is worth double checking, there could be corner cases not covered;
- the test are up-to-date!

## Project Structure ##
To update this structure use this shell command `tree -I "__pycache__|.vscode|.pytest_cache|migrations|db.sqlite3"`.  
You can install `tree` command through `brew install tree`.
```bash
.
├── README.md
├── __init__.py
├── event_manager_test
│   ├── __init__.py
│   ├── app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── views.py
│   ├── asgi.py
│   ├── settings.py
│   ├── templates
│   │   └── swagger-ui.html
│   ├── urls.py
│   ├── utils
│   │   ├── enum.py
│   │   └── exceptions
│   │       ├── __init__.py
│   │       ├── event.py
│   │       └── signup.py
│   └── wsgi.py
├── event_manager_test.postman.json
├── manage.py
├── poetry.lock
├── poetry_scripts.py
├── pyproject.toml
├── pytest.ini
└── tests
    ├── __init__.py
    ├── conftest.py
    └── test_app
        ├── test_event.py
        └── test_user.py
```

At the root folder we can find the configuration files:
- `pyproject.toml`, that is Poetry configuration file;
- `poetry.lock`, that helps resolve dependencies safely;
- `poetry_scripts.py`, python functions used with pyproject.toml script section;
- `manage.py`, Django command line executor;
- `event_manager_test`, as per Django project structure, this is the site:
    - `urls.py`, endpoint definition;
    - `settings.py`, Django project settings.
    - `app`, as per Django project structure, this is an app (and the only one in this case):
        - `admin.py`, Django admin panel configuration;
        - `filters.py`, Django Rest Framework custom filter definition;
        - `models.py`, contains our database table definition through Django ORM;
        - `serializers.py`, Django Rest Framework serializer, a layer between DB and Views/Controllers that translates and validates data;
        - `views.py`, Django views/controllers definition.
    - `utils`, project utilities:
        - `enum.py`, project enums, in this case empty, but I usually setup every project with my CustomEnum base class;
        - `exceptions`, project exceptions:
            - `event.py`, every exception relative to the event concept;
            - `signup.py`, every exception relative to the signup concept.
    - `templates`, HTML templates used by Django:
        - `swagger-ui.html`, default swagger template to display a good API documentation.
- `tests`, project tests:
    - `test_app`, as per Django project structure the test subfolder is called test_<app_name>:
        - `test_event.py`, contains every test relative to the event;
        - `test_user.py`, contains every test relative to the user.
