from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import qsite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///t.sql'
db = SQLAlchemy(app)

@app.route("/user/new")
def createUser():

@app.route("/user/<int:id>/follow")
def followUser(id):
    user = db.session.query(qsite.User).filter(qsite.User.id == id).one()
    user.follow(1, db.session)