from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
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

@app.route("/user/<int:id>/follow")
def followUser(id):
    user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    user.follow(1, db.session)