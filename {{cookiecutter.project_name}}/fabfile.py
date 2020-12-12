"""
Please install fabric3 before run command from this module.
Install fabric3 from console:
>>> python3 -m pip install -U pip
>>> python3 -m pip install -U fabric3
"""


from fabric.api import local, task

DC = "docker-compose -f docker-compose.yml"
DC_STAGE = "docker-compose -f docker-compose-stage.yml"


@task
def build(stage="development"):
    """Run docker-compose build command."""
    if stage == "development":
        local(f"{DC} build")
    else:
        local(f"{DC_STAGE} build")


@task
def start(stage="development"):
    """Run docker-compose."""
    if stage == "development":
        local(f"{DC} up")
    else:
        local(f"{DC_STAGE} up -d")


@task
def stop(stage="development"):
    """Stop docker-compose."""
    if stage == "development":
        local(f"{DC} down")
    else:
        local(f"{DC_STAGE} down")


@task
def logs(stage="development"):
    """Log docker-compose."""
    if stage == "development":
        local(f"{DC} logs")
    else:
        local(f"{DC_STAGE} logs")


@task
def init_db(stage="development"):
    """Db initialiation."""
    if stage == "development":
        local(f"{DC} exec app /bin/bash ./scripts/db_init.sh")
    else:
        local(f"{DC_STAGE} exec app /bin/bash ./scripts/db_init.sh")


# init_db could be split into 2 commands init_db and migrate
# @task
# def migrate():
#     """Db migration."""
#     local(
#         f"{DC} exec app /bin/bash ./scripts/migrate.sh"
#     )

