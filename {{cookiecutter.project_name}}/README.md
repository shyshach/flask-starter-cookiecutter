# {{cookiecutter.project_name}}


## Run locally with docker

Use docker-compose
```
docker-compose up
```


## Initialise environment variables. 

Save `.env.example`  as a `.env` file.
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
fab migrate
```


## Run with gunicorn
For production.
```
cd src && gunicorn main:app
```
