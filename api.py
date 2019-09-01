from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
import qsite

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///t.sql'
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app, model_class = qsite.base)
db.create_all()

@app.route("/user/new", methods = ["PUT"])
def createUser():
    newuser = qsite.User()
    newuser.name = request.json.get("name")
    newuser.description = request.json.get("description", None)
    newuser.email = request.json.get("email")
    newuser.setPassword(request.json.get("password"))
    db.session.add(newuser)
    db.session.commit()
    return json.dumps({"result": "ok", "id": newuser.id})

@app.route("/user/<int:id>/getverifytoken")
def getUserVerifyToken(id):
    # TODO: this is a private API endpoint.
    # Only allow internal frontends to run this.
    user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    if user:
        return json.dumps({"result": "ok", "verifytoken": user.verifytoken})
    else:
        return None

@app.route("/user/<int:id>/verify")
def verifyUser(id):
    user = db.session.query(qsite.User).filter(qsite.User.id == id).one()

    verifytoken = request.args.get("token", None)
    if user.verifytoken == verifytoken:
        user.verified = True
        return json.dumps({"result": "ok"})
    else:
        return None


@app.route("/user/<int:id>/follow")
def followUser(id):
    user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    user.follow(1, db.session)