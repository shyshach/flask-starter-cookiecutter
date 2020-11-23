from sqlalchemy.exc import IntegrityError
from exceptions import ResourceExists
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import pbkdf2_sha256 as sha256


class UserRepository:
    @staticmethod
    def create(username: str, avatar_url: str, password: str) -> dict:
        """ Create user """
        result: dict = {}
        try:
            user = User(
                username=username,
                avatar_url=avatar_url,
                password=UserRepository.generate_hash(password),
            )
            user.save()
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            result = {
                "username": user.username,
                "avatar_url": user.avatar_url,
                "date_created": str(user.date_created),
                "message": "User {} was created".format(user.username),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        except IntegrityError:
            User.rollback()
            raise ResourceExists("user already exists")

        return result

    @staticmethod
    def get(username: str) -> dict:
        """ Query a user by username """
        user: dict = {}
        user = User.query.filter_by(username=username).first_or_404()
        user = {
            "username": user.username,
            "date_created": str(user.date_created),
            "avatar_url": str(user.avatar_url),
            "password": str(user.password),
        }
        return user

    @staticmethod
    def all() -> list:
        users = []
        users = User.query.all()
        return users

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
