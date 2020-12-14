# Flask starter project with cookiecutter

## Requirements
- Docker & Docker-compose
- Python3, cookiecutter
- Fabric3


## Use cookiecutter to make a new project from this template
[Cookiecutter docs](https://cookiecutter.readthedocs.io/en/latest/)
```
pip install --user cookiecutter
cookiecutter https://github.com/shyshach/flask-starter-cookiecutter
```


## Run locally with docker
Build default app in development environment
Use fabric3
```
fab build
fab start
```
You can specify stage
```
fab build:staging
fab start:staging
```

Or use docker-compose (development)
```
docker-compose build
docker-compose up
```


## Run migrations
Replace "staging" with your stagename. If not specified stage is development
```
fab init_db:staging
```

## About .env files
On first run .env.example will be replaced by .env with user-provided data.  
After that .env won't be pushed to GitHub, but .env.sample will
