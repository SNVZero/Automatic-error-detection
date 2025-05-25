from flask_login import UserMixin
from sqlalchemy.orm import relationship

from app import db, manager, app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    models = relationship('GLBModel', backref='user')


class GLBModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    model = db.Column(db.BLOB, nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


