# {{cookiecutter.project_name}}


## Run locally with docker

Use docker-compose
```
docker-compose build
docker-compose up
```


## Initialise environment variables

Check if `.env` file exists. Otherwise save `.env.sample` as a `.env` file and change the values.
Example content:

```
export FLASK_APP="src/main.py"
export POSTGRES_URL="127.0.0.1:5432"
export POSTGRES_DB="mydb"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="example"
export JWT_SECRET_KEY="super-secret"
```


## Run migrations

```
fab init_db
```


## Openapi docs

Go to: http://{{cookiecutter.flask_host}}:{{ cookiecutter.flask_port }}/api/docs/
