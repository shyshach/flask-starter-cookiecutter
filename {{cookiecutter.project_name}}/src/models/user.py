from . import db
from .abc import BaseModel
import datetime


class User(db.Model, BaseModel):
    username = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    avatar_url = db.Column(db.String, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    password = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean)

    def __init__(self, username: str, password: str, active: bool, avatar_url: str = ""):
        self.username = username
        self.avatar_url = avatar_url
        self.password = password
        self.active = active
