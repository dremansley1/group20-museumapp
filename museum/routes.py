from museum import app, db
from flask import Flask, render_template, url_for, request, flash, redirect, session
from museum.models import *
from museum.config import *
from flask_login import login_user, current_user, logout_user, login_required

#page routing setup

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    return render_template("index.html", museum_data = museum_info, page_name = "Museum Map");

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', museum_data = museum_info, page_name = "Settings");
    
@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html', museum_data = museum_info, page_name = "Search");

@app.route("/artifact", methods=['GET', 'POST'])
def artifact():
    return render_template('artifact.html', museum_data = museum_info, page_name = "Artifact");

@app.route("/room_artifacts", methods=['GET', 'POST'])
def room_artifacts():
    return render_template('room_artifacts.html', museum_data = museum_info, page_name = "Artifacts");


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("You have been signed in!")
            return redirect(url_for('mainPage'))
        else:
            flash("Incorrect Login Credentials!")
            return redirect(url_for('login'))
    return render_template('login.html', page_name='Login to Your Account', museum_data = museum_info, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
        email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have been successfully registered") 
        return redirect(url_for('login'))
    return render_template('register.html', page_name='Create an Account', museum_data = museum_info, form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out successfully")
    return redirect(url_for('mainPage'))
