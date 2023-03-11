
from flask import Flask, render_template, redirect, url_for, flash
from my_form import Sign_up_form, Login_form
from flask_sqlalchemy import SQLAlchemy
from flask import request
from database_manager import add_user_in_database, get_user, update_score
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from paragraph_generator import generate_paragraph
from score_calculator import corrector, score_calculator
import time
import os

# setting up the flask app and connecting it to everything
#  we are going to use, database, flask-login

#postgres://super_database_user:MCwWC8nzrvYmGhTMx1ArkgyH79k8upzG@dpg-cg6912pmbg5ab7jrdb00-a.ohio-postgres.render.com/super_database
app = Flask(__name__)
db = SQLAlchemy()
app.secret_key = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


#database structure/class, this is how our table will look like in
# our database, a user is a class in our database and we can 
# access, after getting hold of it, to anything, for example email by typing user.email. 
# the class inherit UserMixin class from Flask-Login to help in our authentification
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique= True, nullable = False)
    password = db.Column(db.String)
    highest_score = db.Column(db.Integer, nullable = False)
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.highest_score = 0
    def get_id(self):
        return super().get_id()
    
# this is to create our database
with app.app_context():
    db.create_all()

#Login_manager is going to manage the login and logout by just getting a particular id
# which in this case is the id from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Route for our main page, first page you will hit
@app.route("/")
def main_page():
    return render_template("index.html")

#This page accept both method
#Get method will simply render the sign up html page to help user log their info in our form
#at the POST method, the infos of user will be extracted from the form
# use those infos and create a unique user with the USER class and put it in our datbase, refer to "class User"
# password are hashed too for safety
@app.route("/SignUp", methods =['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        user = User(user_name= request.form.get('user_name'),
                    email=request.form.get('email'),
                    password=generate_password_hash(password= request.form.get('password'), salt_length=8))
        add_user_in_database(database=db, user_class= user)
        return redirect(url_for('login'))
    form = Sign_up_form()
    return render_template(template_name_or_list='signup.html', form = form )

# GET method display page for login.html to put infos
# Post we will get user using "get_user" function from our database_manager to get User class
# check if everything is fine and log the user in.
# Now current user can access every route that requires login
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method =='POST':
        user = get_user(database_modal=User, email=request.form.get('email'))
        password_entered = request.form.get('password')
        if user and check_password_hash(password= password_entered, pwhash=user.password):
            login_user(user)
            return redirect(url_for('play_game'))
        else:
            flash("you entered the wrong credentials or user don't exist")
            return redirect(url_for('login'))    
    form = Login_form()
    return render_template(template_name_or_list="login.html", form= form)

# This is where the game happens
@app.route('/play_console/', methods=['GET', "POST"])
@login_required
def play_game():
    generated_paragraph = generate_paragraph()
    global tic
    tic = time.perf_counter()
    flash(message="If text don't appear, please press 'restart Button'")
    return render_template(template_name_or_list='typing_window.html', logged_in = True,
                        generated_paragraph = generated_paragraph)

# DISPLAy after corrector function check
#update score if we hit highest score
@login_required
@app.route('/result/<current_paragraph>', methods = ['POST', "GET"])
def result (current_paragraph):
    typed_text = request.form.get('typed_text')
    global toc
    toc = time.perf_counter()
    time_in_seconds = int(toc-tic)-2
    if corrector(typed_text= typed_text, generated_text= current_paragraph ):
        score = score_calculator(typed_text=typed_text, time_in_seconds= time_in_seconds)
        user = get_user(database_modal=User, email= current_user.email)
        if score > user.highest_score:
            update_score(database=db, new_score= score, user = user)
        return render_template(template_name_or_list= 'result.html', correct = True, score = score, time = time_in_seconds, logged_in = True)
    score = 10
    return render_template(template_name_or_list='result.html', score = 10, logged_in = True)

        


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__== "__main__":
    app.run(host = "0.0.0.0", port=5000)


