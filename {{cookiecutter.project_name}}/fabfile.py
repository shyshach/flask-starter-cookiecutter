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
def build(stage="dev"):
    """Run docker-compose build command."""
    if stage == "dev":
        local(f"{DC} build")
    else:
        local(f"{DC_STAGE} build")


@task
def start(stage="dev"):
    """Run docker-compose."""
    if stage == "dev":
        local(f"{DC} up")
    else:
        local(f"{DC_STAGE} up")


@task
def stop(stage="dev"):
    """Stop docker-compose."""
    if stage == "dev":
        local(f"{DC} down")
    else:
        local(f"{DC_STAGE} down")


@task
def logs(stage="dev"):
    """Log docker-compose."""
    if stage == "dev":
        local(f"{DC} logs")
    else:
        local(f"{DC_STAGE} logs")


@task
def init_db():
    """Db initialiation."""
    local(
        f"{DC} exec app /bin/bash ./scripts/db_init.sh"
    )


@task
def migrate():
    """Db migration."""
    local(
        f"{DC} exec app /bin/bash ./scripts/migrate.sh"
    )

@task
def build_stage():
    """deploy to prod"""
    local(
        f"docker-compose -f docker-compose-stage.yml up"
    )