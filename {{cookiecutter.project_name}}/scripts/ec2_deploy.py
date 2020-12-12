import boto3
import os


def generate_pem(ec2_resource, key_file_name):
    with open(f'{key_file_name}.pem', 'w') as outfile:
        keys = ec2_resource.create_key_pair(KeyName=key_file_name, DryRun=False)
        KeyPairOut = str(keys.key_material)
        outfile.write(KeyPairOut)
    os.system(f"chmod 400 {key_file_name}.pem")
    return keys


ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource("ec2")
#pem = generate_pem(ec2_resource, "boto_key3")
user_data = '''#!/bin/bash
yum -y update
yum install -y python3
yum install -y git
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
chkconfig docker on
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
pip3 install cookiecutter
pip3 install fabric3 
cd home
mkdir ec2-user
cd ec2-user
cookiecutter https://github.com/shyshach/flask-starter-cookiecutter.git --no-input
cd test_project
fab start:staging
fab init_db:staging
'''
instances = ec2_resource.create_instances(
    DryRun=False,
    ImageId='ami-04d29b6f966df1537',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='boto_key',
    UserData=user_data
)
print("Instance is being created. Just wait a second")
instances[0].wait_until_running()
ip = instances[0].private_ip_address
public_ip = instances[0].public_ip_address
message = f'''
Use this ip to ssh into your instance {ip}
Example ssh command: ssh -i "boto_key.pem" ec2-user@{ip}
Documentation availble at http://{public_ip}:80/api/docs
You may have to wait for app to start a minute.
'''
with open("server_info.txt", "w+") as f:
    f.write(message)
print(message)
