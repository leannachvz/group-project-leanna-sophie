import requests
import flask_login
import string
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
   userCode = 444

@login_manager.user_loader
def user_loader(username):
    if not user_exists(username):
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('user_id')
    if not email or not user_exists(email):
        return None

    user = User()
    user.id = email
    return user

class UserDB(db.Model):
    username = db.Column(db.String(80), unique=True, primary_key=True, nullable=False)
    password = db.Column(db.String(10), unique=False, nullable=False)
    userCode = db.Column(db.String(10), unique=True)
    friends = db.relationship('Friend', backref='user', lazy = True)

    def __repr__(self) -> str:
        return f"Person with username: {self.username} "

    def get_friends(self):
        return [f.friend_name for f in self.friends]
    

class Friend(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user_db.username'), nullable=False)
    friend_name = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return flask.render_template("welcome.html")

def create_user(username, password):
   characters = string.ascii_letters + string.digits
   while True:
        userCode = ''.join(random.choices(characters, k=4))
        if not code_exists(userCode):
            break
   person = UserDB(username=username, password=password, userCode=userCode)
   db.session.add(person)
   db.session.commit()

   flask_login.current_user.userCode = userCode
   db.session.commit()

@app.route("/login", methods=["POST", "GET"])
def login():
      return flask.render_template("login.html") 

@app.route("/signup", methods=["POST", "GET"])
def sign_up():
   return flask.render_template("signup.html")

@app.route("/login_verification", methods=["POST"])   
def login_verification():
   username = flask.request.form["user_id"]
   userCheck = UserDB.query.filter_by(username=username).first()
   if user_exists(username) and flask.request.form["password"] == userCheck.password:
      user = User()
      user.id = username
      flask_login.login_user(user)
      #flask_login.login_remembered()
      return flask.redirect(flask.url_for("homepage"))
   else:
      flask.flash("Invalid user credential. Try again!")
      return flask.redirect(flask.url_for("login"))

@app.route("/signup_check", methods=["POST"])
def sign_up_check():
   sign_up_username = flask.request.form["user_id"]
   sign_up_password = flask.request.form["password"]
   if user_exists(sign_up_username):# in users:
      flask.flash("That username already exists, enter a different username!")
      return flask.redirect(flask.url_for("sign_up"))
   else:
      create_user(sign_up_username, sign_up_password)
      flask.flash("Sign up was successful! Enter your username to login!")
      return flask.redirect(flask.url_for("login"))
   
@app.route("/home_page")
def homepage():
   username = flask_login.current_user.id
   user = UserDB.query.filter_by(username=username).first()
   code = user.userCode
   
   friends = user.get_friends()

   #f"unique code is {code}"
   return flask.render_template("homepage.html", current_user=username, friends=friends)

@app.route("/convo")
def convo_page():
    return f"hey"

def add_friend(friend_code):
    current_user = flask_login.current_user.id
    user = UserDB.query.filter_by(username=current_user).first()
    friend = UserDB.query.filter_by(userCode=friend_code).first()

    if friend and friend != current_user and friend not in user.friends:
        user.friends.append(friend)
        db.session.commit()
        return True
    else:
        return False
    
@app.route("/add_friend", methods=["POST"])
def add_friend_route():
    friend_code = flask.request.form["friend_code"]
    if add_friend(friend_code):
        flask.flash(f"Friend with code {friend_code} added successfully!")
    else:
        flask.flash(f"Failed to add friend with code {friend_code}.")
    return flask.redirect(flask.url_for("homepage"))

def user_exists(username):
   user = UserDB.query.filter_by(username=username).first()
   if user and user.username == username:
      return True
   else:
      return False

def code_exists(userCode):
    code = UserDB.query.filter_by(userCode=userCode).first()
    if code and code.userCode == userCode:
        return True
    else:
        return False
    
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

app.run()