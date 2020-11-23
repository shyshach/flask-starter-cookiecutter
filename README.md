# {{cookiecutter.project_name}}


## Run locally with docker

Use docker-compose
```
docker-compose up
```
## Go to adminer page
Create there a sequence autoid

## Run migrations

```
fab migrate
```


## Run with gunicorn
For production.
```
cd src && gunicorn main:app
```
