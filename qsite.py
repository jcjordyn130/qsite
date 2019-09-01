import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
import uuid
from passlib.context import CryptContext

engine = sqlalchemy.create_engine("sqlite:///t.sql", echo = True)
base = sqlalchemy.ext.declarative.declarative_base()
newsession = sessionmaker(bind = engine)

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    name = Column(String, index = True, nullable = False)
    description = Column(String)
    email = Column(String, nullable = False)
    verified = Column(Boolean, default = False, nullable = False)
    verifytoken = Column(String)
    passwordhash = Column(String, nullable = False)

    # This is used internally to be able to easily change password hashes.
    _passwordctx = CryptContext(["argon2"])

    def __init__(self):
        # Create a verification token when creating a new user.
        self.verifytoken = uuid.uuid4().hex

    def setPassword(self, plaintext):
        self.passwordhash = self._passwordctx.hash(plaintext)

    def verifyPassword(self, plaintext):
        return self._passwordctx.verify(plaintext, self.passordhash)

    def follow(self, fromuser, session):
        newfollow = Follow()
        newfollow.follower = fromuser.id
        newfollow.followee = self.id
        session.add(follow)

class Follow(base):
    __tablename__ = "followlist"

    id = Column(Integer, primary_key = True, autoincrement = True)
    follower = Column(String, ForeignKey("users.id"), index = True)
    followee = Column(String, ForeignKey("users.id"), index = True)

class Question(base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String, index = True)
    details = Column(String, index = True)
    upvotes = Column(Integer)
    downvotes = Column(Integer)

    def __repr__(self):
        return f"<Question(id='{self.id}', title='{self.title}', details='{self.details}')>"