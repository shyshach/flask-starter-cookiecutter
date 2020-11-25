# {{cookiecutter.project_name}}


## Run locally with docker

Use docker-compose
```
docker-compose up
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
