from . import db
import datetime
from sqlalchemy.exc import IntegrityError


class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), db.ForeignKey('user.username'), nullable=False)
    jti = db.Column(db.String(120))
    blacklisted_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def add(self):
        try:
            db.session.add(self)
            return db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
