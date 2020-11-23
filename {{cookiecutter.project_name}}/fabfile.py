"""
Please install fabric3 before run command from this module.
Install fabric3 from console:
>>> python3 -m pip install -U pip
>>> python3 -m pip install -U fabric3
"""


from fabric.api import local, task

DC = "sudo docker-compose -f docker-compose.yml"


@task
def build():
    """Run docker-compose build command."""
    local(f"{DC} build")


@task
def start():
    """Run docker-compose."""
    local(f"{DC} up")


@task
def stop():
    """Stop docker-compose."""
    local(f"{DC} down")


@task
def logs():
    """Log docker-compose."""
    local(f"{DC} logs")


@task
def migrate():
    """Add migrations and update db."""
    local(
        f"{DC} exec app /bin/bash ./scripts/run_migrations.sh"
    )
