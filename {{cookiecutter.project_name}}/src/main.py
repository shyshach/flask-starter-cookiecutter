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


# CLI for migrations
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=UserModel)
