from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

SECRET_KEY = os.urandom(24)

# Retrieve the API key from environment
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
db = SQLAlchemy(app)

# Database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    history = db.relationship('History', backref='user', lazy=True)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    text = db.Column(db.String(300), unique=False, nullable=False)


# Create database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # Post route
    if request.method == "POST":
        # Check login
        if "username" not in session:
            return redirect(url_for("login"))

        city = request.form.get("city")
        # Ninja API has instructions about how to handle it
        # Documentation here: https://api-ninjas.com/api/weather
        api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            print(response.text)
            data = response.json()
            sunset = datetime.utcfromtimestamp(data["sunset"])
            sunrise = datetime.utcfromtimestamp(data["sunrise"])
            # Add log
            new_log = History(user_id=session["user_id"], city=city, temperature=data["temp"])

            db.session.add(new_log)
            db.session.commit()

            return render_template("dashboard.html", city=city, data=data, username=session["username"], sunset=sunset, sunrise=sunrise)

        else:
            print("Error:", response.status_code, response.text)

    # Get route
    # Check login
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/register", methods=["GET", "POST"])
def register():
    # Post route
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm")
        session.pop('_flashes', None)

        # Username validation
        if len(username) < 3 or len(username) > 30:
            flash("Username must be between 3 and 30 characters", "danger")
            return redirect(url_for("register"))

        # Password validation
        if len(password) < 8 or len(password) > 128:
            flash("Password must be longer than 8 characters", "danger")
            return redirect(url_for("register"))
        if password == username:
            flash("Password can't be the equal to the username", "danger")
            return redirect(url_for("register"))

        # Email validation
        if len(email) < 5 or len(email) > 254:
            flash("Email must be longer than 5 characters", "danger")

        # Confirm password validation
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        # Add new user
        new_user = Users(username=username, email=email, password=generate_password_hash(password))

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("success"))
        # Error handling
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists", "danger")
            return redirect(url_for("register"))

    # Get route
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Post route
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember_checkbox = request.form.get("remember")

        # Check password
        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["username"] = user.username
                if remember_checkbox:
                    session.permanent = True
                session.pop('alert', None)
                return redirect(url_for("dashboard"))
            else:
                flash("The password you entered is incorrect.", "danger")
        else:
            flash("The username you entered doesn't exist.", "danger")

    # Get route
    if "username" in session:
        return redirect(url_for("dashboard"))
    session.pop('alert', None)
    return render_template("login.html")

@app.route("/history")
def history():
    history = History.query.filter_by(user_id=session["user_id"]).order_by(History.time.desc()).all()
    return render_template("history.html", history=history)


@app.route("/board", methods=["GET", "POST"])
def board():
    if request.method == "POST":
        username = session["username"]
        text = request.form.get("text")

        # Add text to db
        new_user = Messages(username = username, text = text)
        db.session.add(new_user)
        db.session.commit()

        messages = Messages.query.order_by(Messages.id.desc()).limit(50).all()

        return render_template("board.html", messages=messages)

    messages = Messages.query.order_by(Messages.id.desc()).limit(50).all()
    return render_template("board.html", messages=messages)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        username = session["username"]
        current_password = request.form.get("password")
        new_password = request.form.get("new_password")

        # Password validation
        if len(new_password) < 8 or len(new_password) > 128:
            flash("Password must be longer than 8 characters", "danger")
            return redirect(url_for("settings"))

        # Find user
        user = Users.query.filter_by(username=username).first()

        if user:
            # Compare password
            if check_password_hash(user.password, current_password):
                # Update password
                user.password = generate_password_hash(new_password)
                db.session.commit()

                # Update session
                session["password"] = user.password
                flash("Password updated", "success")
                return redirect(url_for("logout"))
            else:
                flash("Incorrect password", "danger")
        else:
            flash("User not found", "danger")

    return render_template("settings.html")


@app.route("/logout")
def logout():
    if "username" in session:
        session.clear()
        # Remove the permanent session cookie
        session.modified = True
        return render_template("login.html", logout="You have been successfully logged out")
    return redirect(url_for("login"))


@app.route("/success")
def success():

    if "username" in session:
        return redirect(url_for("dashboard"))

    return render_template("success.html")


if __name__ == "__main__":
    app.run()
