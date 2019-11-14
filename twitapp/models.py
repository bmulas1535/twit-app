from twitapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    usergroup = db.Column(db.String(6), nullable=False, default="REG")
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)


class Tuser(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    newest_tweet_id = db.Column(db.BigInteger)


class Tweets(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Unicode(300))
    embedding = db.Column(db.PickleType, nullable=False)
    tuser_id = db.Column(db.BigInteger,
                         db.ForeignKey('tuser.id'),
                         nullable=False)
    tuser = db.relationship('Tuser', backref=db.backref('tweets', lazy=True))
