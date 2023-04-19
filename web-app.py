import requests
import flask_login
from os import getenv
from dotenv import load_dotenv, find_dotenv
import json
import random
import flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv()) #loads .env file in path

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

app.secret_key = "6942069"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'doggy@yay.com': {'password': 'secret'}}

class User(flask_login.UserMixin):
   pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

class UserDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieID = db.Column(db.String(80), unique= False, nullable=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    comment = db.Column(db.String(150), unique=False, nullable=True)
    rating = db.Column(db.String(3), unique=False, nullable=True)

    def __repr__(self) -> str:
        return f"Person with username: {self.username} and email: {self.comment} and blood: {self.rating}"

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return flask.render_template("welcome.html")

def create_user(username):
   users.append(username)
   person = UserDB(username=username)
   db.session.add(person)
   db.session.commit()
   
def create_feedback(movieID, user, newComment, rating):
   new_feedback = UserDB(movieID=movieID, username=user, comment=newComment, rating=rating)
   db.session.add(new_feedback)
   db.session.commit()
   people = UserDB.query.all()
   return repr(people)
   

@app.route("/login", methods=["POST", "GET"])
def login():
      return flask.render_template("login.html")
   

@app.route("/signup", methods=["POST", "GET"])
def sign_up():
   return flask.render_template("signup.html")

app.run(DEBUG=True)