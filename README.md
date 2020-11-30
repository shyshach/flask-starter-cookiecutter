# Flask starter project with cookiecutter

## Requirements
- Docker & Docker-compose
- Python3, cookiecutter
- Fabric3 (optional)


## Use cookiecutter to make a new project from this template
[Cookiecutter docs](https://cookiecutter.readthedocs.io/en/latest/)
```
pip install --user cookiecutter
cookiecutter https://github.com/shyshach/flask-starter-cookiecutter
```


## Run locally with docker

Use docker-compose
```
docker-compose up
```

## Run migrations

```
fab init_db
fab migrate
```
## About .env files
On first run .env.example will be replaced by .env with user-provided data.  
After that .env won't be pushed to GitHub, but .env.sample will
