from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm.exc
import json
from . import database as qsite
from . import errors

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///t.sql'
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app, model_class = qsite.base)
db.create_all()

# This is the handler function so flask can work with error.py errors.
@app.errorhandler(errors.APIError)
def handleError(exc):
    return exc.json, exc.httpcode

@app.route("/v0/user/new", methods = ["PUT"])
def createUser():
    newuser = qsite.User()
    newuser.name = request.json.get("name")
    newuser.description = request.json.get("description", None)
    newuser.email = request.json.get("email")
    newuser.setPassword(request.json.get("password"))
    db.session.add(newuser)
    db.session.commit()

    return json.dumps({"id": newuser.id})

@app.route("/v0/user/<int:id>/getverifytoken")
def getUserVerifyToken(id):
    # TODO: this is a private API endpoint.
    # Only allow internal frontends to run this.
    try:
        user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        raise errors.NoUserFoundError()

    return json.dumps({"verifytoken": user.verifytoken})

@app.route("/v0/user/<int:id>/verify")
def verifyUser(id):
    try:
        user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        raise errors.NoUserFoundError()

    verifytoken = request.args.get("token", None)
    if user.verifytoken == verifytoken:
        user.verified = True
        user.verifytoken = None
    else:
        raise errors.InvalidVerifyToken()

    db.session.commit()
    raise errors.NoError()

@app.route("/v0/user/<int:id>/follow")
def followUser(id):
    user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    user.follow(1, db.session)
