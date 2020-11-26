from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from repositories import UserRepository
from models.revoked_token import RevokedToken
from sqlalchemy.exc import IntegrityError


class User(Resource):
    def get(self, username: str):
        user = UserRepository.get(username)
        return user, 200


class UserList(Resource):
    def post(self):
        """Create user."""
        request_json = request.get_json(silent=True)
        username: str = request_json.get('username')
        avatar_url: str = request_json.get('avatar_url', '')
        password: str = request_json.get('password')
        try:
            user = UserRepository.create(username, avatar_url, password)
            return user, 200
        except Exception as e:
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response

    def get(self):
        """ Get users list."""
        users_query = UserRepository.all()
        if len(users_query):
            users = []
            for user in users_query:
                users.append(
                    {
                        "username": user.username,
                        "avatar": user.avatar_url,
                        "created": str(user.date_created),
                    }
                )
        else:
            users = {}
        return users, 200


class UserLogin(Resource):
    def post(self):
        request_json = request.get_json(silent=True)
        username: str = request_json["username"]
        password: str = request_json.get("password")
        # lookup by username
        if UserRepository.get(username):
            current_user = UserRepository.get(username)
        else:
            return {"message": "User {} doesn't exist".format(username)}, 404

        if UserRepository.verify_hash(password, current_user["password"]):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                "message": "Logged in as {}".format(current_user["username"]),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        else:
            return {"message": "Wrong password"}, 401


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedToken(jti=jti, username=get_jwt_identity())
            revoked_token.add()
            return {"message": "Access token has been revoked"}, 200
        except IntegrityError:
            return {"message": "Something went wrong while revoking token"}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # id of a jwt accessing this post method
        try:
            revoked_token = RevokedToken(jti=jti, username=get_jwt_identity())
            revoked_token.add()
            return {"message": "Refresh token has been revoked"}, 200
        except IntegrityError:
            return {"message": "Something went wrong while revoking token"}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_identity = get_jwt_identity()
        access_token = create_access_token(identity=current_user_identity)
        return {"access_token": access_token}
