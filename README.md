# {{cookiecutter.project_name}}


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
