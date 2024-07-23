import datetime, hashlib, os
import bcrypt #password hashing library
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    #user fields:
    email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False) #stored hash
    #token fields:
    session_token  = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    refresh_token = db.Column(db.String, nullable=False, unique=True)


    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password_digest = bcrypt.hashpw((kwargs.get('password').encode()), bcrypt.gensalt(rounds=13))
        self.renew_session() #generates and initializes the token fields


    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest() #returns a random long hex number
    
    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=2)
        self.refresh_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_digest)

    def verify_session_token(self, token):
        expired = datetime.datetime.now() >= self.session_expiration
        return token == self.session_token and not expired

    def verify_refresh_token(self, token):
        return token == self.refresh_token

