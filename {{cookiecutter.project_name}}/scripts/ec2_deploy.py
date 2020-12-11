import boto3
import os


def generate_pem(ec2_resource, key_file_name):
    with open(f'{key_file_name}.pem', 'w') as outfile:
        keys = ec2_resource.create_key_pair(KeyName=key_file_name)
        KeyPairOut = str(keys.key_material)
        # print(KeyPairOut)
        outfile.write(KeyPairOut)
    os.system(f"chmod 400 {key_file_name}.pem")
    return keys




ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource("ec2")
pem = generate_pem(ec2_resource, "test2")
user_data = '''#!/bin/bash
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
# print(instances)
# print(pem)
