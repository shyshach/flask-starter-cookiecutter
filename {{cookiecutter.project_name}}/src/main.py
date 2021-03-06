import os
import subprocess
import yaml

from flask import render_template
from flask_migrate import Migrate
from flask_restful import Api

from app import create_app
from models import User as UserModel, db
from resources import (
    HealthCheck,
    UserList,
    User,
    UserLogin,
    UserLogoutAccess,
    UserLogoutRefresh,
    TokenRefresh,
    PasswordChange
)


app = create_app()
migrate = Migrate(app, db)


# API
api = Api(app)
api.add_resource(PasswordChange, "/api/change_password")
api.add_resource(HealthCheck, "/healthcheck")
api.add_resource(User, "/api/users/<username>")
api.add_resource(UserList, "/api/users/")
api.add_resource(UserLogin, "/api/login")
api.add_resource(UserLogoutAccess, "/api/logout_access")
api.add_resource(UserLogoutRefresh, "/api/logout_refresh")
api.add_resource(TokenRefresh, "/api/refresh")


# Custom openapi docs route
@app.route('/api/docs/')
def openapi():
    """Return Swagger UI for custom openapi.yaml in static/openapi.yaml."""
    return render_template('swagger.html')


@app.before_first_request
def before_first_request():
    if os.getenv("ENV") != "dev":
        ip = os.popen("curl http://checkip.amazonaws.com").read().strip()
        app.logger.info(f"Checking server`s IP address {ip}")
        open_api_yaml = "/app/src/static/swagger/openapi.yaml"
        with open(open_api_yaml, "r+") as f:
            file = yaml.load(f, Loader=yaml.FullLoader)
            file["servers"][0]["url"] = file["servers"][0]["url"].replace("0.0.0.0", f"{ip}")
        with open(open_api_yaml, "w") as f:
            yaml.dump(file, f, default_flow_style=False)

        app.logger.info("Run DB migrations")
        subprocess.run(["chmod", "a+rwx", "/app/scripts/db_init.sh"])
        p = subprocess.Popen(
            "/app/scripts/db_init.sh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        out, err = p.communicate()
        app.logger.info(f"OUT: {out}")
        app.logger.info(f"Err: {err}")


# CLI for migrations
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=UserModel)
