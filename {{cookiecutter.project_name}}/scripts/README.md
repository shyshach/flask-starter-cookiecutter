# Deploy to EC2 instance script

## Requirements
- Configured AWS account [Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

## Just run ec2_deploy.py script
```
python3 ec2_deploy.py
```

## Wait a minute for instance to be started
Then you will get notofied about public and private IP of your instance. Also that information will be duplicated into server_info.txt file.
After that you have to ssh into your instance and run fab init_db:'stagename' for migrations
Voila, your service is up and running

## Warning:
If you assign an Elastic IP to your EC2 instance, you have to change it in src/static/swagger/openapi.yaml file.
