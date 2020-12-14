from configparser import ConfigParser
from datetime import datetime
import os
import time

import boto3
from botocore.config import Config
import click


def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def generate_key_name(prefix="boto_key"):
    key_name = str(time.time()).replace(".", "")
    if prefix:
        key_name = f"{prefix}_{key_name}"
    return key_name


def generate_pem(ec2_resource, key_file_name):
    base_dir = os.getcwd()
    filename = f'{key_file_name}.pem'
    full_path = os.path.join(base_dir, "keys", filename)
    try:
        os.stat(os.path.join(base_dir, "keys"))
    except Exception:
        os.mkdir(os.path.join(base_dir, "keys"))
    if os.path.isfile(full_path):
        click.secho("Pem file already exists!!!", fg='red')
        keys = None
    else:
        with open(full_path, 'w') as outfile:
            keys = ec2_resource.create_key_pair(KeyName=key_file_name, DryRun=False)
            KeyPairOut = str(keys.key_material)
            outfile.write(KeyPairOut)
        click.secho(f"\nPem file '{filename}' created successfully!!!\n", fg='blue')
        os.system(f"chmod 400 {full_path}")
    return keys


def write_message(ip, public_ip, key_name):
    message = f'''
    Use this ip to ssh into your instance {ip}
    Example ssh command: ssh -i "keys/{key_name}.pem" ec2-user@{public_ip}
    Documentation available at http://{public_ip}/api/docs
    You may have to wait for app to start a minute.
    '''
    with open("server_info.txt", "w+") as f:
        f.write(message)
    print(message)


BASH_CMDS = '''#!/bin/bash
sudo yum update -y && yum install -y python3 git
sudo yum install -y https://s3.region.amazonaws.com/amazon-ssm-region/latest/linux_amd64/amazon-ssm-agent.rpm
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
sudo service docker restart
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo python3 -m pip install -U pip && sudo python3 -m pip install -U cookiecutter fabric3
mkdir -p /home/ec2-user/app
cd /home/ec2-user/app
git clone {repo_name} .
sudo cp .env.sample .env
fab build:staging
fab start:staging
'''


def generate_initial_commands(repo_name):
    return BASH_CMDS.format(repo_name=repo_name)


def main(repo_name=None):
    my_config = Config(
        region_name=os.getenv("AWS_DEFAULT_REGION", "eu-central-1"),
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    boto3.client(
        'ec2',
        config=my_config,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    ec2_resource = boto3.resource("ec2")
    key_name = generate_key_name()
    pem = generate_pem(ec2_resource, key_name)
    image_id = "ami-0bd39c806c2335b95"
    if pem and repo_name:
        commands = generate_initial_commands(repo_name=repo_name)
        instances = ec2_resource.create_instances(
            DryRun=False,
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=key_name,
            UserData=commands,
        )
        click.echo(
            click.style(
                "Instance is being created. Just wait a few seconds",
                blink=True,
                bold=True
            )
        )
        instances[0].wait_until_running()
        instance_id = instances[0].id
        time.sleep(5)
        instance = ec2_resource.Instance(instance_id)
        ip = instance.private_ip_address
        public_ip = instance.public_ip_address
        click.secho(f"\nInstance ID: {instance_id}", fg='green')
        click.secho(f"Instance public IP: {public_ip}", fg='green')
        write_message(ip, public_ip, key_name)
        click.echo(
            click.style(
                "\n Please wait until ec2 instance will install all requirements\n",
                blink=True,
                bold=False
            )
        )
        items = list(range(0, 49))
        for item in progressBar(items, prefix='Progress:', suffix='Complete', length=50):
            time.sleep(2)

        config = ConfigParser()
        config_file = "deploy.ini"
        # read values from a section
        # config.read(config_file)
        # string_val = config.get('section_a', 'string_val')
        # bool_val = config.getboolean('section_a', 'bool_val')
        # int_val = config.getint('section_a', 'int_val')
        # float_val = config.getfloat('section_a', 'pi_val')
        config.add_section('initial_deploy')
        config.set('initial_deploy', 'date', str(datetime.now()))
        config.set('initial_deploy', 'instance_id', instance_id)
        config.set('initial_deploy', 'key_file_name', key_name)
        config.set('initial_deploy', 'public_ip', public_ip)
        config.set('initial_deploy', 'internal_ip', ip)
        config.set('initial_deploy', 'project_repo', repo_name)
        ssh_cmd = f"ssh -i keys/{key_name}.pem ec2-user@{public_ip}"
        config.set('initial_deploy', 'ssh_command', ssh_cmd)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


if __name__ == "__main__":
    PROJECT_REPO = os.getenv("PROJECT_REPO", "")
    repo_name = click.prompt("Please enter a project's repository", default=PROJECT_REPO)
    if repo_name:
        main(repo_name=repo_name)
    else:
        click.secho("Can't deploy an application without source code", fg='red')
