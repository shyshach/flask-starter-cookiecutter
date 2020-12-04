import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()


def setup_jwt(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    jwt = JWTManager(app)

    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

    from models.revoked_token import RevokedToken

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        return RevokedToken.is_jti_blacklisted(jti)


def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    db.init_app(app)
    setup_jwt(app)
    CORS(app)
    return app
