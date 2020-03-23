import os
from museum import app, db
from flask import Flask, render_template, url_for, request, flash, redirect, session
from museum.models import *
from museum.forms import *
from museum.config import *
from flask_login import login_user, current_user, logout_user, login_required
#from sqlalchemy import create_engine
from sqlalchemy import *


@app.route("/", methods=['GET', 'POST'])
def mainpage():
    return render_template("index.html", museum_data = museum_info, page_name = "Cardiff Museum");

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', museum_data = museum_info, page_name = "Settings");
    
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = ArtPieceSearchForm()
    search = ArtPieceSearchForm(request.form)
    if request.method == 'POST':
        artPieces = []
        search_string = search.data['search']
        if search.data['search'] != '':
            search_string = '%{0}%'.format(search_string)
            artPieces = ArtPiece.query.filter(or_(  ArtPiece.title.like(search_string), ArtPiece.description.like(search_string))) 

           #### result = ArtPiece.query.join(Artist).filter(Artist.artist_name.like(search_string) ).all()

          #  re=ArtPiece.query.outerjoin(Artist, ArtPiece.c.artist_id == Artist.c.artist_id)


            return render_template('search.html', artPieces=artPieces,museum_data = museum_info, page_name = "Search", form=form);        
    artPieces = ArtPiece.query.all()
    return render_template('search.html', artPieces=artPieces, museum_data = museum_info, page_name = "Search", form=form);

##################################


@app.route("/artifact/<int:artwork_id>", methods=['GET', 'POST'])
def artifact(artwork_id):
    artPiece = ArtPiece.query.get_or_404(artwork_id)
    return render_template('artifact.html', artPiece = artPiece, museum_data = museum_info, page_name = "Artifact");

@app.route("/room/<int:room_id>", methods=['GET', 'POST'])
def room(room_id):
    room = Room.query.get_or_404(room_id)
    page_name = "Room " + str(room.room_id)
    return render_template('room.html', museum_data = museum_info, page_name = page_name, room = room);

@app.route("/scan", methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        qr_code = request.form['scan']
        if qr_code != '':
            result = ArtPiece.query.get_or_404(qr_code)
            return render_template('artifact.html', artPiece = result, museum_data = museum_info, page_name = "Artifact");        
    return render_template('scan.html', museum_data = museum_info, page_name = "Scan");

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("You have been signed in!")
            return redirect(url_for('mainPage'))
        else:
            flash("Incorrect Login Credentials!")
            return redirect(url_for('login'))
    return render_template('login.html', page_name='Admin Login', museum_data = museum_info, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_login = user(username=form.username.data,
        email=form.email.data, password=form.password.data)
        db.session.add(user_login)
        db.session.commit()
        flash("You have been successfully registered") 
        return redirect(url_for('login'))
    return render_template('register.html', page_name='Create an Account', museum_data = museum_info, form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out successfully")
    return redirect(url_for('mainPage'))
