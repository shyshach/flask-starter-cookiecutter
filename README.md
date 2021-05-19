# Flask starter project with cookiecutter

## Requirements
- Docker & Docker-compose
- Python3, cookiecutter
- Fabric3


## Use cookiecutter to make a new project from this template
[Cookiecutter docs](https://cookiecutter.readthedocs.io/en/latest/)
```
pip install --user cookiecutter
# for using fabric3 commands from fabfile install it first
# example command for fabric3 installation: pip install fabric3
cookiecutter https://github.com/shyshach/flask-starter-cookiecutter.git
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
Replace "staging" with your stagename. If not specified stage is dev
```
fab init_db:staging
```

## About .env files
On first run .env.example will be replaced by .env with user-provided data.  
After that .env won't be pushed to GitHub, but .env.sample will.    
If you deploy your project to EC2 instance be sure than .env.sample contains the same info as your local .env(apart from info about your AWS account)

## Deploy project to ec2 AMI instance (WARNING: only first time deploy.)
After setting up project locally, add your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env file.     
Then push your project to GIT repository and specify your repository url in PROJECT_REPO in .env file.      
Run fab start ot docker-compose up    
Then in project directory run   
```
fab deploy
```
The keys to instance will be generated in keys directory as well as ini file with deploy configuration and instructions about how to connect to your instance. 

Then wait a couple of minutes and go to EC2 console on AWS, find there your newly created instance and change security group configuration to accept HTTP requests.          
Then wait a couple of minutes and check the Swagger docs url provided in generated server_info.txt.  
If you want to change instance configuration check scripts/ec_deploy.py.   
## Warning 
If you assign an Elastic IP to your EC2 instance, you have to change it in src/static/swagger/openapi.yaml file.
Also once in a while EC2 instance's IP may change.  


