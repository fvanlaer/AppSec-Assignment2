from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database import db
from loginman import login


class User(UserMixin, db.Model):

    # User properties
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    phone = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    # We need to "link" user to their text submission(s)
    texts = db.relationship('Text', backref='author', lazy='dynamic')

    def set_password(self, password, phone):
        self.password_hash = generate_password_hash(password + phone)

    def check_password(self, password, phone):
        return check_password_hash(self.password_hash, password + phone)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Text(db.Model):

    # Text submission properties
    id = db.Column(db.Integer, primary_key=True)
    before_spellcheck = db.Column(db.String(140))
    after_spellcheck = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Text {}>'.format(self.before_spellcheck)


# Loading user from database
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
